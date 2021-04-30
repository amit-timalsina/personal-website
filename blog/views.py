from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.conf import settings

from .models import *
from .forms import PostForm
from .filters import PostFilter
# Create your views here.

def posts(request):
    posts = Post.objects.filter(active=True)
    trending_posts = Post.objects.filter(trending=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')

    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {'posts': posts, 'trending_posts': trending_posts, 'myFilter': myFilter}
    return render(request, 'blog/blog.html', context)

def post(request, slug):
    post = Post.objects.get(slug=slug)

    # Comment section
    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        messages.success(request, 'Your comment was sucessfully posted!')
        
        return redirect('post', slug=post.slug)

    context = {'post': post}
    return render(request, 'blog/post.html', context)




# CRUD VIEWS

@admin_only
@login_required(login_url='home')
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')
    
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)

@admin_only
@login_required(login_url='home')
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid:
            form.save()
        return redirect('posts')
    
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)

def deletePost(request, slug):
    post = Post.objects.get(slug=slug)
    
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item': post}
    return render(request, 'blog/delete.html')