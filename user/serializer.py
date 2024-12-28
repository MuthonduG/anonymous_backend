from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'anonymous_unique_id']

    def validate_email(self, value):
        """Custom email validation."""
        if not value.endswith("@usiu.ac.ke"): 
            raise serializers.ValidationError("Only @usiu.ac.ke emails are allowed.")
        return value

    def create(self, validated_data):
        """Override create method to handle password hashing."""
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Override update method to handle password hashing."""
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
