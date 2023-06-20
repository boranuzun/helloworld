from django.contrib.auth.models import Group
from backend.users.models import CustomUser
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, permissions
from .models import Event, Interested_In_Event, Place, Comment
from .serializers import UserSerializer, GroupSerializer, ReadEventSerializer, WriteEventSerializer, Interested_In_EventSerializer, PlaceSerializer, CommentReadSerializer, CommentWriteSerializer, Interested_In_EventSerializerByEvent

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = ReadEventSerializer
    # SHOULD IMPLEMENT CUSTOM PERMISSIONS FOR OBJECT LEVEL SECURITY
    permission_classes = [permissions.AllowAny]

    # Returns a different Serializer for Read and Write requests
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"] :
            return WriteEventSerializer
        return ReadEventSerializer
    
    # Returns a different queryset if request contains specific parameters
    def get_queryset(self):
        title = self.request.query_params.get('title')
        user_id = self.request.query_params.get('user_id')

        if title:
            queryset = Event.objects.filter(title__contains = title)
        elif user_id:
            queryset = Event.objects.filter(user_id__contains = user_id)
        else:
            queryset = Event.objects.all()
        return queryset

    
class Interested_In_EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows interested_in_event to be viewed or edited.
    """
    queryset = Interested_In_Event.objects.all()
    serializer_class = Interested_In_EventSerializer
    permission_classes = [permissions.AllowAny]

    # Returns a different Serializer if specific parameters in request
    def get_serializer_class(self):
        if  'event' in self.request.query_params:
            return Interested_In_EventSerializerByEvent
        return Interested_In_EventSerializer

    # Returns a different queryset if request contains specific parameters
    def get_queryset(self):
        user = self.request.query_params.get('user')
        event = self.request.query_params.get('event')
        if user:
            queryset = Interested_In_Event.objects.filter(user__pk = user)
            answers_list = list(queryset)
            queryset = answers_list
        elif event:
            queryset = Interested_In_Event.objects.filter(event__pk = event)
            answers_list = list(queryset)
            queryset = answers_list
        else:
            queryset = Interested_In_Event.objects.all()
        return queryset

class PlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows places to be viewed or edited.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.AllowAny]

    # Returns a different queryset if request contains specific parameters
    def get_queryset(self):
        venue_name = self.request.query_params.get('venue_name')
        city = self.request.query_params.get('city')
        state = self.request.query_params.get('state')
        zip = self.request.query_params.get('zip')

        if venue_name:
            queryset = Place.objects.filter(venue_name__contains = venue_name)
        elif city:
            queryset = Place.objects.filter(city__contains = city)
        elif state:
            queryset = Place.objects.filter(state__contains = state)
        elif zip:
            queryset = Place.objects.filter(zip__contains = zip)
        else:
            queryset = Place.objects.all()
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer
    permission_classes = [permissions.AllowAny]

    # Returns a different Serializer for Read and Write requests
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"] :
            return CommentWriteSerializer
        return CommentReadSerializer
    
    # Returns a different queryset if request contains specific parameters
    def get_queryset(self):
        event = self.request.query_params.get('event')
        
        if event:
            queryset = Comment.objects.filter(event = event)
        else:
            queryset = Comment.objects.all()
        return queryset