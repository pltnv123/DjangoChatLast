from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView
from django.urls import reverse

from rest_framework import viewsets
import logging

from .models import Room, Message, Profile
from .forms import CreateRoomForm, ProfilePictureForm

from .serializers import RoomSerializer, MessageSerializer, ProfileSerializer


@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


@login_required
def room(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    messages = Message.objects.filter(room=room).order_by('-date_added')[:25]

    # Get the list of users in the room
    online_users = room.users.all()
    logging.debug(f"online_users: {online_users}")

    return render(request, 'room.html', {'room': room, 'messages': messages, 'online_users': online_users})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    profile_query = Profile.objects.filter(user=user)
    if profile_query.exists():
        profile = profile_query.first()
        picture = profile.picture
    else:
        picture = None

    return render(request, 'user_profile.html', {'user': user, 'picture': picture})


class DeleteRoom(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'delroom.html'
    success_url = reverse_lazy('rooms')

    slug_url_kwarg = 'room_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        context['room'] = room
        print(room.slug)  # Здесь "value" - это атрибут объекта комнаты, который вы хотите вывести
        return context

    def get_success_url(self):
        return reverse_lazy('rooms')


class CreateRoom(LoginRequiredMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'CreateRoom.html'


def edit_photo(request):
    Profile = get_user_model().profile.related.related_model

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect(reverse('user_profile', args=[request.user.username]))
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'edit_photo.html', {'form': form})


def edit_nickname(request):
    user = request.user

    if request.method == 'POST':
        new_nickname = request.POST.get('nickname')
        user.username = new_nickname
        user.save()

        return redirect(reverse('user_profile', args=[user.username]))
    else:
        return render(request, 'edit_nickname.html', {'user': user})


###################


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
