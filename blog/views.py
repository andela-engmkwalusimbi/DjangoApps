from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post
from .forms import PostForm

def posts_create(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': 'Create Post',
        'form': form,
    }
    return render(request, 'post_form.html', context)


def posts_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context_data = {
        'title': 'Detail',
        'post': post
    }
    return render(request, 'post_detail.html', context_data)


def posts_list(request):
    queryset = Post.objects.all()
    paginator = Paginator(queryset, 10) # Show 10 contacts per page

    page_req = 'page'
    page = request.GET.get(page_req)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    context_data = {
        'title': 'List',
        'posts': posts,
        'page_req': page_req
    }
    return render(request, 'post_list.html', context_data)


def posts_update(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post Updated')
        return HttpResponseRedirect(instance.get_absolute_url())

    context_data = {
        'title': 'Post update',
        'post': post,
        'form': form
    }
    return render(request, 'post_form.html', context_data)


def posts_delete(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Post Deleted')
    return redirect('blogs:list')
