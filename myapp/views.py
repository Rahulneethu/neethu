from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post
from .form import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login')
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'post_list.html',{'posts':posts})

@login_required(login_url='/account/login')
def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    return render(request,'post_detail.html',{'post':post})

@login_required(login_url='/account/login')
def post_new(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)

    else:
     form=PostForm()
    return render(request,'post_edit.html',{'form':form})

@login_required(login_url='/account/login')
def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        form=PostForm(request.Post,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm(instance=post)
    return render(request,'post_edit.html',{'form':form})

def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')