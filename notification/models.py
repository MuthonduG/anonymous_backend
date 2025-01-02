from django.db import models
from django.conf import settings

class Notification(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SENT = 'SENT', 'Sent'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    issue_id = models.CharField(max_length=150, unique=True, blank=True, null=True)
    notification_header = models.CharField(max_length=150)
    notification_message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    recipient_email = models.EmailField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    def __str__(self):
        return f"{self.notification_header} : {self.issue_id}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
