from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'image']


class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'is_host', 'is_owner']


class EventInteractionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = EventInteraction
        fields = ['id', 'user', 'liked', 'saved']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'timestamp', 'accuracy', 'source']

class AppUserSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = AppUser
        fields = [
            'username', 'fullname', 'email', 'bio',
            'mobile_number', 'profile_picture', 'location',
            'is_active', 'is_staff', 'date_joined', 'last_login'
        ]

class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)
    host_owner = AppUserSerializer()
    location = LocationSerializer()
    participants = ParticipantSerializer(many=True, read_only=True)
    interactions = EventInteractionSerializer(source='event_interactions', many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'thumbnail', 'images', 'description', 'rating',
            'host_owner', 'location', 'is_private', 'needs_id', 'date_created', 
            'date_start', 'date_closed', 'date_ended','seats', 'price', 'open_status',
            'tags', 'participants', 'interactions'
        ]

class UserFollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()

    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'following', 'date_followed']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # You can add custom claims here if you want
        token['username'] = user.username
        token['email'] = user.email

        return token

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = AppUser
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = AppUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
