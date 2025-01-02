from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'issue_id',
            'notification_header',
            'notification_message',
            'sent_at',
            'recipient_email',
            'uploaded_at',
            'status',
        ]
        read_only_fields = ['user', 'sent_at', 'uploaded_at', 'status']
