from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views import View
from django.contrib import messages
from .models import Post, Comment
from .forms import LoginForm, SignupForm
from.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



def signupView(request):
    """ Signup view """
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Thanks for registering. You are now logged in.")
                return redirect('/login/')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})


def loginView(request):
    """ Login view """
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})



@login_required(login_url="/login")
def user_logout(request):
    """ Logout view """
    logout(request)
    return redirect('/login/')



@login_required(login_url="/login")
def index(request):
    posts_list = Post.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html',{'posts':posts})



@login_required(login_url="/login")
def view_post(request, id):
    """ VIEW Posts """
    post = Post.objects.filter(id=id).first()

    comments =  Comment.objects.filter(post=post)
    if request.method == "POST":
        data  = request.POST
        name  = data.get('name')
        body  = data.get('body')
        email = data.get('email')

        try:
            # post = Post.objects.get()
            comment = Comment.objects.create(
                name  = name,
                email = email,
                body  = body,
                post  = post,
                user  = request.user
            )
            return redirect('/')
        except Exception as e:
            return HttpResponse(str(e))

    return render(request,'post.html',{'posts':post, "comments":comments})


def share_post(request):
    """ share post """

    data=request.POST
    name=data.get('name')
    comments=data.get('comments')
    email=data.get('email')
    to=data.get('to')
    url=data.get('url')

    context = {
        'name': name,
        'email': email,
        'comments': comments,
        'to': to,
        "url" :url
        }
    template = render_to_string('email_content.html', {'request':request,'context': context})
    try:
        email = EmailMessage(  
                        "My post", template, to=[to]  
            )  
        email.send()
    except BadHeaderError:
        return HttpResponse('Failed Please Try Again ')

    return redirect('/')

