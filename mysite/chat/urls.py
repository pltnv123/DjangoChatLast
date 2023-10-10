from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from .views import DeleteRoom, CreateRoom, edit_photo

urlpatterns = [
                  path("", views.rooms, name="rooms"),
                  path('edit_photo/', edit_photo, name='edit_photo'),

                  path('users/<str:username>/', views.user_profile, name='user_profile'),

                  path("create/", CreateRoom.as_view(), name="room_create"),
                  path("<str:room_name>/", views.room, name="room"),
                  path("<str:room_name>/delete/", DeleteRoom.as_view(), name='room_delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
