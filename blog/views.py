from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Post
from .forms import PostForm


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

    theme = request.COOKIES.get('theme', 'light')
    if theme not in ['light', 'dark']:
        theme = 'light'

    context = {
        'posts': posts,
        'search_query': search_query,
        'sort_query': sort_query,
        'total_count': posts.count(),
        'theme': theme,
    }
    return render(request, 'blog/home.html', context)


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

    theme = request.COOKIES.get('theme', 'light')
    if theme not in ['light', 'dark']:
        theme = 'light'

    context = {
        'form': form,
        'theme': theme,
    }
    return render(request, 'blog/add_post.html', context)


def post_detail(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id, is_published=True)

    theme = request.COOKIES.get('theme', 'light')
    if theme not in ['light', 'dark']:
        theme = 'light'

    context = {
        'post': post,
        'theme': theme,
    }
    return render(request, 'blog/post_detail.html', context)


def set_theme(request, mode: str):
    mode = mode.lower()
    if mode not in ['light', 'dark']:
        mode = 'light'

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        next_url = '/'

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
