from rest_framework import serializers
from .models import Report

class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

    image_data = serializers.FileField(required=False)
    audio_data = serializers.FileField(required=False)
    video_data = serializers.FileField(required=False)

    def validate_image_data(self, value):
        if value is not None:  # Validate only if there is a file
            valid_extensions = ['jpg', 'jpeg', 'png']
            if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                raise serializers.ValidationError("Only image files (JPG, JPEG, PNG) are allowed.")
            if value.size > 52428800:
                raise serializers.ValidationError("File size too large. Maximum is 50 MB.")
        return value

    def validate_audio_data(self, value):
        if value is not None:  # Validate only if there is a file
            valid_extensions = ['mp3', 'wav', 'aac']
            if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                raise serializers.ValidationError("Only audio files (MP3, WAV, AAC) are allowed.")
            if value.size > 52428800:
                raise serializers.ValidationError("File size too large. Maximum is 50 MB.")
        return value

    def validate_video_data(self, value):
        if value is not None:  # Validate only if there is a file
            valid_extensions = ['mp4', 'avi', 'mkv']
            if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                raise serializers.ValidationError("Only video files (MP4, AVI, MKV) are allowed.")
            if value.size > 52428800:
                raise serializers.ValidationError("File size too large. Maximum is 50 MB.")
        return value
