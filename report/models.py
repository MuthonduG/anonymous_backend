from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from cloudinary.models import CloudinaryField

# Create your models here.
class Report(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    report_title = models.CharField(max_length=150)
    report_type = models.CharField(max_length=150)
    report_description = models.CharField(max_length=1000)
    report_status = models.BooleanField(default=False)
    image_data = CloudinaryField('image') 
    audio_data = CloudinaryField('audio')  
    video_data = CloudinaryField('video')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_title}:{self.report_status}"
