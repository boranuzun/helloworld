from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Event, Interested_In_Event, Place, Comment
from backend.users.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'email', 'groups', 'profilePic', 'username']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class Interested_In_EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interested_In_Event
        fields = ['pk', 'event', 'user']

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'venue_name', 'address', 'zip', 'city', 'state', 'creator']

class ReadEventSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_pic', 'date', 'event_capacity', 'price', 'creator', 'place']

class WriteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_pic', 'date', 'event_capacity', 'price', 'creator', 'place']

class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profilePic']

class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'event', 'user', 'msg']

class CommentReadSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
   
    class Meta:
        model = Comment
        fields = ['pk', 'event', 'user', 'msg', 'created_at']

class Interested_In_EventSerializerByEvent(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
   
    class Meta:
        model = Interested_In_Event
        fields = ['user']