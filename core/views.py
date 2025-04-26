from rest_framework import viewsets
from .models import Event, AppUser, UserFollow, Participant, EventInteraction
from .serializers import EventSerializer, AppUserSerializer, UserFollowSerializer, ParticipantSerializer, EventInteractionSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

class UserFollowViewSet(viewsets.ModelViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class EventInteractionViewSet(viewsets.ModelViewSet):
    queryset = EventInteraction.objects.all()
    serializer_class = EventInteractionSerializer