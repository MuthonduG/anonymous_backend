from django.urls import path
from .views import NotificationViewSet

urlpatterns = [
    path('notifications/', NotificationViewSet.as_view({'get': 'list', 'post': 'create'}), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='notification-detail'),
    path('notifications/<int:pk>/send/', NotificationViewSet.as_view({'post': 'send'}), name='notification-send'),
    path('notifications/send_all/', NotificationViewSet.as_view({'post': 'send_all'}), name='notification-send-all'),
]
