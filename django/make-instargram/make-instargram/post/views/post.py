from django.shortcuts import render, get_object_or_404, redirect

from post.forms.post import PostForm
from post.forms import CommentForm
from post.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():

            # post = form.save(commit=False)
            # post.author = request.user
            # post.save()

            post = form.save(author=request.user)
            post.save()

            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_modify(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()
        return redirect('post:post_list')
    return render(request, 'post/post_delete.html')


def post_like_toggle(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    post_like, post_like_created = post.postlike_set.get_or_create(
        user=request.user,
    )

    if not post_like_created:
        post_like.delete()

    return redirect('post:post_detail', post_pk=post.pk)


