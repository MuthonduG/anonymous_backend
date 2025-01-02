from celery import shared_task
from django.core.mail import send_mail
from .models import Notification
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_email(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        subject = notification.notification_header
        message = notification.notification_message
        sender_email = "muthondugithinji@gmail.com"
        recipient = [notification.recipient_email]

        send_mail(subject, message, sender_email, recipient, fail_silently=False)
        notification.status = 'SENT'
        notification.save()
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send email for Notification {notification_id}: {e}")
