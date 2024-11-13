from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceListView, UserListView, DeviceCreateView, ChatMessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

# Register your viewsets
router.register(r'api/chat', ChatMessageViewSet)
urlpatterns = [
    path('devices/', DeviceListView.as_view(), name='device-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('devices/add/', DeviceCreateView.as_view(), name='device-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
