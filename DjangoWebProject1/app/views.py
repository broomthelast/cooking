"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .forms import RatingFormCoolEdition
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm
from django.urls import reverse

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Ваша контактная страница',
            'year':datetime.now().year,
        }
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year':datetime.now().year,
        }
    )

def links(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ссылки',
            'year':datetime.now().year,
        }
    )

def pool(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = RatingFormCoolEdition(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            context = {
                'pool_data': cleaned_data,
                'form': None,
                }
            return render(request, 'app/success.html', context)
        else:
            context = {'form': form,'pool_data': None}
            return render(request, 'app/pool.html', context)
    else:
        form = RatingFormCoolEdition()
        context = {
            'title': 'Оставить отзыв',
            'year': datetime.now().year,
            'form': form,
            'pool_data': None,
        }
        return render(request, 'app/pool.html', context)

def success(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/success.html',
        {
            'title':'Спасибо за отзыв!',
            'year':datetime.now().year,
        }
    )

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            return redirect('home')

        else:
            return render(request, 'app/registration.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'app/registration.html', {'form': form})

def blog(request):
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(request,'app/blog.html',
    {
        'title':'Блог',
        'posts': posts,
        'year':datetime.now().year,
    })


def blogpost(request, parametr):
    assert isinstance(request, HttpRequest)
    post1 = get_object_or_404(Blog, id=parametr)
    comments = Comment.objects.filter(post=post1).order_by('-date')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post1 
            comment.author = request.user
            comment.date = datetime.now()
            comment.save()
            return redirect('blogpost', parametr=post1.id)
    else:
        form = CommentForm()

    context = {
        'post1': post1,
        'year': datetime.now().year,
        'comments': comments,
        'form': form,
    }

    return render(request, 'app/blogpost.html', context)

def new_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save()
            return redirect(reverse('blogpost', kwargs={'parametr': blog_post.id}))
    else:
        form = BlogForm()
    return render(request, 'app/newpost.html', {'form': form})


def video(request):
    videos = [
        {'name1': 'Видео 1', 'url1': '/media/nbc.mp4'},
        {'name2': 'Видео 2', 'url2': '/media/dcm.mp4'},
    ]
    return render(request, 'app/video.html', {'videos': videos})