from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogPost, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth


def home(request):
    blogs = Blog.objects
    blog_list=Blog.objects.all()
    paginator = Paginator(blog_list,3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request,'home.html', {'blogs':blogs,'posts':posts})

def detail(request,blog_id):
    detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html',{'detail':detail})

def new(request):
    return render(request, 'new.html') 
    
def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()

    return redirect('/blog/'+str(blog.id))
def blogpost(request):
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date=timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'new.html',{'form':form})

def update(request, pk):
    blog = get_object_or_404(Blog, pk = pk)
    form = BlogPost(request.POST,instance=blog)

    if form.is_valid():
       form.save()
       return redirect('home')

    return render(request, 'new.html',{'form':form})


def delete(request, pk):
    blog = get_object_or_404(Blog, pk = pk)
    blog.delete()
    return redirect('home')

def addcomment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
           comment = form.save(commit=False)
           comment.post = blog
           comment.save()
           return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'addcomment.html', {'form':form})

    #url 은 항상 문자열임
# Create your views here.
