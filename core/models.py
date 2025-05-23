import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from datetime import datetime


class Event(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    images = models.ManyToManyField('EventImage', blank=True, related_name='event_images')
    description = models.TextField()
    rating = models.FloatField()
    host_owner = models.ForeignKey('AppUser', related_name='event', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    is_private = models.BooleanField(default=False, verbose_name="Private event")
    needs_id = models.BooleanField(default=False, verbose_name="Identification")
    date_created = models.DateTimeField(default=timezone.now)
    date_start = models.DateTimeField()
    date_closed = models.DateTimeField()
    date_ended = models.DateTimeField(default=datetime(2100, 1, 1, 0, 0, 0))
    seats = models.IntegerField()
    price = models.FloatField()
    open_status = models.BooleanField(default=True, verbose_name="Event open")
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    def __str__(self):
        return f"{self.title} - ({self.id})"
    
class EventImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, related_name='event_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events_images/')
    date_uploaded = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Event Image'
        verbose_name_plural = 'Event Images'

    def __str__(self):
        return f"Image for {self.event.title}"
    
class EventInteraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='event_interactions', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)
    date_interacted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = 'Event Interaction'
        verbose_name_plural = 'Event Interactions'

    def __str__(self):
        if self.liked and self.saved:
            return f"{self.user.fullname} saved and liked {self.event.title}"
        elif self.saved:
            return f"{self.user.fullname} saved {self.event.title}"
        else:
            return f"{self.user.fullname} liked {self.event.title}"
        
class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    accuracy = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"Located at {self.name}"

class AppUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(primary_key=True, max_length=150, unique=True)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    mobile_number = models.CharField(max_length=8, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', max_length=100, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='users', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.fullname

    def __str__(self):
        return f"{self.fullname} - ({self.username})"
    
class UserFollow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(AppUser, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(AppUser, related_name='following', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'User Interaction'
        verbose_name_plural = 'User Interactions'

    def __str__(self):
        return f"{self.follower.fullname} follows {self.following.fullname}"
    
class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    date_participated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.is_owner:
            return f"{self.user.fullname} owns and is hosting {self.event.title}"
        elif self.is_host and not self.is_owner:
            return f"{self.user.fullname} is hosting {self.event.title}"
        else:
            return f"{self.user.fullname} is participating in {self.event.title}"