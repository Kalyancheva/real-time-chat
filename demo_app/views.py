from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic,Message
from .forms import RoomForm


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exists')
            

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password are incorrect')
        

    return render(request,'demo_app/login_register.html',{'page':page})

def registerpage(request):
    page = "register"
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'an error in registering')
    return render(request,'demo_app/login_register.html',{'page':page,'form':form})

def logoutuser(request):
    logout(request)
    return redirect('/login')


def home(request):

    q = request.GET.get('q') if request.GET.get('q')!= None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(desc__icontains=q)|
        Q(host__username__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    print(room_messages)
    return render(request,'demo_app/main.html',{'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages})

def rooms(request,pk):
    # ls = [
    #     {'id':1,'name':'web-dev'},
    #     {'id':2,'name':'app-dev'},
    #     {'id':3,'name':'ML-dev'},
    # ]
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method=='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('rooms',pk=room.id)
    return render(request,"demo_app/rooms.html",{'rooms':room, 'room_messages':room_messages,'participants':participants})

def userprofile(request,pk):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages =user.message_set.filter(room__topic__name__icontains=q)
   
    return render(request,'demo_app/profile.html',{'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages})


@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)  # Use the submitted data
        if form.is_valid():
            room = form.save(commit=False)  # Save without saving to database yet
            room.host = request.user
            room.save()  # Explicitly save the room object
            return redirect('home')  # Redirect to appropriate URL

    context = {'form': form}
    return render(request, "demo_app/room_info.html", context)
@login_required(login_url='login')
def UpdateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Requid permissions")

    if request.method == 'POST':
        form = RoomForm(request.POST)  # Use the submitted data
        if form.is_valid():
            room = form.save(commit=False)  # Save without saving to database yet
            room.save()  # Explicitly save the room object
            return redirect('home')  # Redirect to appropriate URL


    context = {'form': form}
    return render(request, "demo_app/room_info.html", context)


@login_required(login_url='login')
def DeleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Requid permissions")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'demo_app/delete.html',{'obj':room.name})
@login_required(login_url='login')
def DeleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("Requid permissions")
    if request.method == 'POST':
        message.delete()
        return redirect('/rooms/'+str(message.room.id))
    return render(request,'demo_app/delete.html',{'obj':message.body})


# Create your views here.
