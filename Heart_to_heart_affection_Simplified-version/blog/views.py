from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator

@login_required(login_url='/user/login')
def blog_page(request):
    search_query = request.GET.get('search', '')  # 获取搜索关键词

    if search_query:
        posts_list = Post.objects.filter(title__icontains=search_query).order_by('-created_at')  # 模糊搜索
    else:
        posts_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts_list, 5)  # 每页显示5篇文章
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    for post in posts:
        post.limited_comments = post.comments.all()[:3]  # 限制评论数量

    if request.method == 'POST':
        if 'post_form' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                return redirect('blog_page')

        elif 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                post = get_object_or_404(Post, pk=request.POST.get('post_id'))
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect('post_detail', pk=post.pk)
    else:
        post_form = PostForm()
        comment_form = CommentForm()

    return render(request, 'blog/blog_page.html', {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'search_query': search_query,  # 传递搜索关键词到模板
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        # 获取 next 参数，默认重定向到帖子列表
    next_url = request.GET.get('next', '/blog/')  # 默认返回首页
    page = request.GET.get('page', 1)

    # 确保 next_url 里包含 page 信息
    if 'page=' not in next_url:
        next_url += '?' + urlencode({'page': page})

    return redirect(next_url)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # 确保只有作者可以删除帖子
    if request.user == post.author:
        post.delete()
        return redirect('/blog/')  # 重定向到帖子列表页面
    else:
        return redirect('/blog/')  # 如果不是作者，重定向回去
