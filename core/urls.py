from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'users', AppUserViewSet, basename='user')
router.register(r'user-follows', UserFollowViewSet, basename='userfollow')
router.register(r'participants', ParticipantViewSet, basename='participant')
router.register(r'event-interactions', EventInteractionViewSet, basename='eventinteraction')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserAPIView.as_view(), name='current_user'),
    path('register/', RegistrationView.as_view(), name='register')
]
