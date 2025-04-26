from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, AppUserViewSet, UserFollowViewSet, ParticipantViewSet, EventInteractionViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', AppUserViewSet)
router.register(r'user-follows', UserFollowViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'event-interactions', EventInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
