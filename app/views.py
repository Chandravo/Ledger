from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Room, money_request, receipt

import random
import string

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
    user=request.user
    rooms=list(user.user_rooms.all())
    
    
    return render(request, 'home.html', {'name': user.name, 'rooms': rooms})

@login_required(login_url='/login')
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        room_password = request.POST['room_password']
        room_key = ''.join(random.choice(string.digits) for i in range(6))
        while (Room.objects.filter(key=room_key).exists()):
            room_key = ''.join(random.choices(string.digits) for i in range(6))
        room = Room.objects.create(key=room_key, name=room_name, password=room_password, creator=request.user)
        room.users.add(request.user)
        room.save()
        return render(request,'room_created.html', {'room_key': room_key, 'room_name': room_name,'room_password': room_password})
    else: 
        return render(request, 'create_room.html')
    
@login_required(login_url='/login')
def join_room(request):
    if request.method == 'POST':
        room_key = request.POST['room_key']
        room_password = request.POST['room_password']
        if Room.objects.filter(key=room_key).exists():
            room = Room.objects.get(key=room_key)
            if room.password == room_password:
                room.users.add(request.user)
                room.save()
                return redirect('/room/'+room_key)
            else:
                messages.add_message(request, messages.ERROR, "Wrong password!")
                return render(request, 'join_room.html')
        else:
            messages.add_message(request, messages.ERROR, "Room does not exist!")
            return render(request, 'join_room.html')
    else:
        return render(request, 'join_room.html')


@login_required(login_url='/login')
def room(request,room_key):
    if (Room.objects.filter(key=room_key).exists()):
        room=Room.objects.get(key=room_key)
        if (request.user in room.users.all()):
            room = Room.objects.get(key=room_key)
            users=room.users.all()
            return render(request, 'room.html', {'room': room, 'users': users, 'curr_user': request.user})
        else:
            error="You are not in this room!"
            return render(request, 'no_room.html', {'error': error})
        
    else:
        error="Room does not exist!"
        return render(request, 'no_room.html', {'error': error})
    
@login_required(login_url='/login')
def delete_room(request, room_key):
    if (Room.objects.filter(key=room_key).exists()):
        room=Room.objects.get(key=room_key)
        if (request.user == room.creator):
            room.delete()
            return redirect('/')
        else:
            error = "You are not the creator of this room!"
            return render(request, 'no_room.html', {'error': error})
    else:
        error = "Room does not exist!"
        return render(request, 'no_room.html', {'error': error})
    
@login_required(login_url='/login')
def create_money_request(request,room_key):
    if request.method == 'POST':
        room_key = request.POST['room_key']
        amount = request.POST['amount']
        description = request.POST['description']
        to_user_email = request.POST['to_user']
        to_user=User.objects.get(email=to_user_email)
        if Room.objects.filter(key=room_key).exists():
            room = Room.objects.get(key=room_key)
            if (request.user in room.users.all()):
                req = money_request.objects.create(room=room, amount=amount, description=description, from_user=request.user, to_user=to_user)
                req.save()
                return redirect('/room/'+room_key)
            else:
                error="You are not in this room!"
                return render(request, 'no_room.html', {'error': error})
        else:
            error="Room does not exist!"
            return render(request, 'no_room.html', {'error': error})
    else:
        room = Room.objects.get(key=room_key)
        from_user = request.user
        users = room.users.all()
        return render(request, 'create_money_request.html', {'room_key': room_key, 'from_user': from_user, 'users': users})