from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
import logging

from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView

from .models import Room, Message
from .forms import CreateRoomForm, ProfilePictureForm


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
    return render(request, 'user_profile.html', {'user': user})


class DeleteRoom(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'delroom.html'
    success_url = reverse_lazy('rooms')

    slug_url_kwarg = 'room_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('rooms')


class CreateRoom(LoginRequiredMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'CreateRoom.html'


def edit_photo(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfilePictureForm(instance=request.user.profile)

    return render(request, 'edit_photo.html', {'form': form})
