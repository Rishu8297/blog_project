from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseBadRequest
from app1.forms import *
from app1.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request,'app1/home.html',{'posts':posts})

def about(request):
    return render(request,'app1/about.html')

def contact(request):
    return render(request,'app1/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'app1/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return redirect(reverse('login'))

def user_logout(request):
    logout(request)
    return redirect('/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request,data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname,password = upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Welcome {}!'.format(uname))
                    return redirect(reverse('dashboard'))
                else: 
                    return HttpResponseBadRequest('Invalid Credentials')
            else: 
                return HttpResponseBadRequest('Invalid Credentials')
        else:
            form  = LoginForm()
        return render(request,'app1/login.html',{'form':form})
    else:
        return redirect(reverse('dashboard'))

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You are ready to become an author')
            user = form.save()
            user_wala_grp = Group.objects.get(name='Author')
            user.groups.add(user_wala_grp)
            return redirect(reverse('login'))
    else:
        form  = SignUpForm()
    return render(request,'app1/signup.html',{'form':form})


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postform = PostForm(request.POST)
            if postform.is_valid:
                # title = postform.cleaned_data['title']
                # desc = postform.cleaned_data['desc']
                # post = Post(title=title,desc=desc)
                postform.save()
                return redirect(reverse('dashboard'))
            else:
                return HttpResponseBadRequest('Invalid Post')    
        else:
            postform  = PostForm()
            return render(request,'app1/addPost.html',{'Postform':postform})
    else:
        return redirect(reverse('login'))
    

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid:
                form.save()
                return redirect(reverse('dashboard'))
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
            return render(request,'app1/updatePost.html',{'Postform':form})
    else:
        return redirect(reverse('login'))
    
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return redirect(reverse('dashboard'))
    else:
        return redirect(reverse('login'))
    


