from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Room, Message, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class RoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ['name', 'slug', 'users']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ['room', 'user', 'content', 'date_added']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'picture']
