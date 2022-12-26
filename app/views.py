from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Room, money_request, receipt


import datetime
import random
import string

def register(request):
    if (request.method == 'POST'):
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        if (User.objects.filter(email=email).exists()):
            error = "Email already exists!"
            return render(request, 'no_room.html', {'error': error})
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
def logout(request):
    auth.logout(request)
    return redirect('/')

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
            in_req = money_request.objects.filter(room=room, to_user=request.user, is_accepted=False).order_by('-date')
            out_req = money_request.objects.filter(room=room, from_user=request.user, is_accepted=False).order_by('-date')
            out_rec = receipt.objects.filter(room=room, from_user=request.user)
            in_rec = receipt.objects.filter(room=room, to_user=request.user)
            return render(request, 'room.html', {'room': room, 'users': users, 'curr_user': request.user,'in_req': in_req, 'out_req': out_req, 'in_rec': in_rec, 'out_rec': out_rec})
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
def accepted_money_requests(request,room_key):
    room = Room.objects.get(key=room_key)
    in_req = money_request.objects.filter(room=room, to_user=request.user, is_accepted=True).order_by('-date')
    out_req = money_request.objects.filter(room=room, from_user=request.user, is_accepted=True).order_by('-date')
    return render(request, 'a_m_r.html', {'in_req': in_req, 'out_req': out_req})

    
@login_required(login_url='/login')
def create_money_request(request,room_key):
    if request.method == 'POST':
        room_key = request.POST['room_key']
        amount = int(request.POST['amount'])
        if (amount<0):
            return render(request, 'no_room.html', {'error': "Amount must be positive!"})
        description = request.POST['description']
        to_user_email = request.POST['to_user']
        to_user=User.objects.get(email=to_user_email)
        if Room.objects.filter(key=room_key).exists():
            room = Room.objects.get(key=room_key)
            if (request.user in room.users.all()):
                request_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
                while (money_request.objects.filter(key=request_key).exists()):
                    request_key = ''.join(random.choices(string.ascii_letters + string.digits) for _ in range(20))
                req = money_request.objects.create(room=room, amount=amount, description=description, from_user=request.user, to_user=to_user, key=request_key)
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
    
@login_required(login_url='/login')
def delete_money_request(request):
    if request.method == 'POST':
        request_key = request.POST['request_key']
        room_key = request.POST['room_key']
        if (money_request.objects.filter(key=request_key).exists()):
            req = money_request.objects.get(key=request_key)
            if (req.from_user == request.user):
                req.delete()
                
    return redirect('/room/'+room_key)

@login_required(login_url='/login')
def accept_money_request(request):
    if request.method == 'POST':
        request_key = request.POST['request_key']
        room_key = request.POST['room_key']
        room = Room.objects.get(key=room_key)
        req = money_request.objects.get(key=request_key)
        if (receipt.objects.filter(room=room, from_user=req.from_user, to_user=req.to_user ).exists()):
            rec = receipt.objects.get(room=room, from_user=req.from_user, to_user=req.to_user )
            rec.amount += req.amount
            rec.save()
            # rec.date=datetime.datetime.now()
           
            req.status="accepted"
        elif (receipt.objects.filter(room=room, from_user=req.to_user, to_user=req.from_user ).exists()):
            rec = receipt.objects.get(room=room, from_user=req.to_user, to_user=req.from_user )
            rec.amount -= req.amount
            # rec.date=datetime.datetime.now()
            rec.save()
           
        else:
            rec = receipt.objects.create(room=room, from_user=req.from_user, to_user=req.to_user, amount=req.amount)
            rec.save()
            
            
        
        req.is_accepted=True
        req.save()     
    return redirect('/room/'+room_key)

        
    
        