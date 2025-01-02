from django.contrib import admin
from django.core.mail import send_mail
from django.contrib import messages
from .models import Notification
from .tasks import send_notification_email
import logging

logger = logging.getLogger(__name__)

@admin.action(description="Send selected notifications")
def send_notifications(modeladmin, request, queryset):
    success_count = 0
    failure_count = 0

    for notification in queryset.filter(status='PENDING'):
        try:
            send_notification_email.delay(notification.id)  # Use Celery task for async email
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to trigger email for Notification {notification.id}: {e}")
            failure_count += 1

    modeladmin.message_user(
        request,
        f"Notifications sent successfully: {success_count}, Failed: {failure_count}",
        level=messages.SUCCESS if failure_count == 0 else messages.WARNING,
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_header', 'status', 'sent_at')
    actions = [send_notifications]

    def has_permission(self, request, perm):
        return request.user.is_staff and request.user.has_perm(f'notifications.{perm}')

    def has_module_permission(self, request):
        return self.has_permission(request, 'view_notification')

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, 'change_notification')

    def has_add_permission(self, request):
        return self.has_permission(request, 'add_notification')

    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, 'delete_notification')
