from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class AppUserViewSet(viewsets.ModelViewSet):
    serializer_class = AppUserSerializer

    def get_queryset(self):
        return AppUser.objects.filter(is_superuser=False)

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AppUserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
class RegistrationView(generics.CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = RegistrationSerializer

class UserFollowViewSet(viewsets.ModelViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class EventInteractionViewSet(viewsets.ModelViewSet):
    queryset = EventInteraction.objects.all()
    serializer_class = EventInteractionSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer