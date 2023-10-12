from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings

from rest_framework.routers import DefaultRouter
from chat.views import RoomViewSet, MessageViewSet, ProfileViewSet

router = DefaultRouter()
router.register('rooms', RoomViewSet, basename='users')
router.register('messages', MessageViewSet, basename='group')
router.register('profiles', ProfileViewSet, basename='messages')

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('', include('accounts.urls')),
                  path("rooms/", include("chat.urls")),
                  path("api/", include(router.urls))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
