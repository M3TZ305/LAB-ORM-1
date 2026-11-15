from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Post
from .forms import PostForm


def legacy_lang_redirect(request, lang, subpath=''):
    response = redirect('/' + subpath)
    response.set_cookie('django_language', lang, path='/', samesite='Lax')
    return response


def home(request):
    search_query = request.GET.get('search', '').strip()
    sort_query = request.GET.get('sort', 'latest').strip().lower()

    posts = Post.objects.filter(is_published=True)

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    if sort_query == 'oldest':
        posts = posts.order_by('published_at', 'id')
    else:
        sort_query = 'latest'
        posts = posts.order_by('-published_at', '-id')

    context = {
        'posts': posts,
        'search_query': search_query,
        'sort_query': sort_query,
        'total_count': posts.count(),
    }
    return render(request, 'blog/home.html', context)


def about(request):
    context = {}
    return render(request, 'blog/about.html', context)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_published = True
            post.save()
            return redirect('blog:home')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/add_post.html', context)


def post_detail(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id, is_published=True)

    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)


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
