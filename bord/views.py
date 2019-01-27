from django.utils import timezone
from .models import Post, PostViews
from .forms import PostForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'bord/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not PostViews.objects.filter(post=post, session=request.session.session_key):
        view = PostViews(post=post,
                         ip=request.META['REMOTE_ADDR'],
                         created=timezone.now(),
                         session=request.session.session_key)
        view.save()
    postview = PostViews.objects.filter(post=post).count()
    return render(request, 'bord/post_detail.html', context={'post': post, 'postview': postview})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'bord/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'bord/post_edit.html', {'form': form})
