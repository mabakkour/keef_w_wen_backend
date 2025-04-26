from rest_framework import serializers
from .models import AppUser, Event, EventImage, Participant, EventInteraction, UserFollow


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


class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    interactions = EventInteractionSerializer(source='eventinteraction_set', many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'thumbnail', 'images', 'description', 'rating',
            'host_owner', 'distance', 'location', 'latitude', 'longitude',
            'is_private', 'needs_id', 'date_created', 'date_start', 'date_closed',
            'seats', 'price', 'open_status', 'tags', 'participants', 'interactions'
        ]


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            'id', 'username', 'fullname', 'email', 'bio',
            'mobile_number', 'profile_picture',
            'is_active', 'is_staff', 'date_joined', 'last_login'
        ]


class UserFollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()

    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'following', 'created_at']
