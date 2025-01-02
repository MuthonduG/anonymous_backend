from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification_email

class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notification instances.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only see their own notifications
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current logged-in user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """
        Custom endpoint to send a specific notification.
        """
        notification = get_object_or_404(Notification, pk=pk, user=request.user)

        if notification.status == Notification.StatusChoices.SENT:
            return Response({"detail": "Notification already sent."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_notification_email.delay(notification.id)
            return Response({"detail": "Notification is being sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Failed to send notification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
