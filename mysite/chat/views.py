from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
import logging

from .models import Room, Message


# def index(request):
#     return render(request, "index.html")
#
#
# def room(request, room_name):
#     return render(request, "room.html", {"room_name": room_name})


@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


# @login_required
# def room(request, room_name):
#     room = Room.objects.get(slug=room_name)
#     # Получаем первые 25 сообщений
#     messages = Message.objects.filter(room=room)[0:25]
#     return render(request, 'room.html', {'room': room, 'messages': messages})


@login_required
def room(request, room_name):
    room = Room.objects.get(slug=room_name)
    messages = Message.objects.filter(room=room).order_by('-date_added')[:25]

    # Get the list of users in the room
    online_users = room.users.all()
    logging.debug(f"online_users: {online_users}")

    return render(request, 'room.html', {'room': room, 'messages': messages, 'online_users': online_users})
