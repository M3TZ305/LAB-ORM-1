from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import resolve, Resolver404
from django.views.decorators.http import require_http_methods, require_POST
from .models import Post
from .forms import PostForm
from media_library.services import save_article

def legacy_redirect(request, subpath='home/'):
    while subpath.startswith(('ar/', 'en/')): subpath = subpath[3:]
    target = '/' + subpath.lstrip('/')
    try:
        match = resolve(target)
        if match.namespace not in ['blog'] or match.url_name == 'set_theme': raise Http404
    except Resolver404: raise Http404
    query = request.GET.urlencode()
    return redirect(target + ('?' + query if query else ''))

def home(request):
    search = request.GET.get('search','').strip()
    sort = 'oldest' if request.GET.get('sort') == 'oldest' else 'latest'
    posts = Post.objects.filter(is_published=True).prefetch_related('attachments')
    if search: posts = posts.filter(Q(title__icontains=search)|Q(content__icontains=search))
    posts = posts.order_by('published_at','id') if sort == 'oldest' else posts.order_by('-published_at','-id')
    return render(request,'blog/articles.html' if request.resolver_match.url_name == 'articles' else 'blog/home.html',{'posts':posts,'search_query':search,'sort_query':sort})
def about(request): return render(request,'blog/about.html')

@require_http_methods(['GET','POST'])
def article_form(request, post_id=None):
    post = get_object_or_404(Post,pk=post_id) if post_id else None
    if post and not post.is_published: raise Http404
    form = PostForm(request.POST if request.method == 'POST' else None, request.FILES if request.method == 'POST' else None, instance=post)
    if request.method == 'POST' and form.is_valid():
        try:
            saved = save_article(form, request.user)
        except OSError:
            form.add_error(None,'تعذر حفظ المرفقات. يرجى إعادة المحاولة واختيار الملفات مجددًا.')
        else:
            messages.success(request,'تم تحديث المقال.' if post else 'تم نشر المقال.')
            return redirect('blog:home')
    return render(request,'blog/add_post.html',{'form':form,'post':post,'current_time':timezone.now()})
add_post = article_form
edit_post = article_form

def post_detail(request,post_id):
    post=get_object_or_404(Post.objects.prefetch_related('attachments'),pk=post_id)
    if not post.is_published: raise Http404
    return render(request,'blog/post_detail.html',{'post':post})

@require_http_methods(['GET','POST'])
def delete_post(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    if not post.is_published: raise Http404
    if request.method == 'POST':
        from django.db import transaction
        with transaction.atomic(): post.delete()
        messages.success(request,'تم حذف المقال.')
        return redirect('blog:home')
    return redirect('blog:post_detail',post_id=post.pk)

@require_POST
def set_theme(request, mode: str):
    mode = mode.lower()
    if mode not in ['light', 'dark']:
        mode = 'light'

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/home/'
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        next_url = '/home/'

    response = redirect(next_url)

    max_age = 30 * 24 * 60 * 60
    response.set_cookie(
        key='theme',
        value=mode,
        max_age=max_age,
        path='/',
        samesite='Lax',
        httponly=False
    )
    return response
