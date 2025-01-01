from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    issue_id = models.CharField(max_length=150)
    notification_header = models.CharField(max_length=150)
    notification_message = models.CharField(max_length=1000)
    sent_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_header}:{self.issue_id}"
    
class EmailNotification(models.Model):
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="email_notifications")
    user_email = models.EmailField()
    pass
