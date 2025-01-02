from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Notification

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_email_notification(sender, instance, **kwargs):
    notifications = Notification.objects.filter(user=instance, status='PENDING')

    for notification in notifications:
        try:
            subject = notification.notification_header
            message = notification.notification_message
            sender_email = "muthondugithinji@gmail.com"
            recipient = [notification.recipient_email]

            send_mail(subject, message, sender_email, recipient, fail_silently=False)
            
            # Update notification status to SENT
            notification.status = 'SENT'
            notification.save()
        except Exception as e:
            print(f"Failed to send email: {e}")

