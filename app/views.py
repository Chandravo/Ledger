from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def register(request):
    if (request.method == 'POST'):
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        user = User.objects.create_user(email=email, password=password, name=name)
        user.save()
        return redirect('login')
    else:
        return render(request, 'register.html')

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, "Wrong username or password!")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')


    

