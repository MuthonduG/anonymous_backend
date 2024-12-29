from rest_framework import serializers
from .models import Report

class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report  
        fields = '__all__'

    def validate_image_data(self, value):
        valid_extensions = ['jpg', 'jpeg', 'png']
        if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError("Only image files (JPG, JPEG, PNG) are allowed.")
        return value

    def validate_audio_data(self, value):
        valid_extensions = ['mp3', 'wav', 'aac']
        if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError("Only audio files (MP3, WAV, AAC) are allowed.")
        return value

    def validate_video_data(self, value):
        valid_extensions = ['mp4', 'avi', 'mkv']
        if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError("Only video files (MP4, AVI, MKV) are allowed.")
        return value

    def validate_report_type(self, value):
        allowed_types = ['type1', 'type2', 'type3']  # Example allowed types
        if value not in allowed_types:
            raise serializers.ValidationError(f"Report type must be one of {allowed_types}.")
        return value
