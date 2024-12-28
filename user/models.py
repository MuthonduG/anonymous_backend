from django.core.exceptions import ValidationError
from django.db import models
import hashlib
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    anonymous_unique_id = models.CharField(max_length=256, editable=False)
    security_query_response = models.CharField(max_length=256)

    def clean(self):
        # Validate email uniqueness.
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'This email address is already in use.'})

    def generate_anonymous_id(self):
        # Create a unique anonymous id.
        combined_string = f"{self.security_query_response}:{self.email}"
        anonymous_id = hashlib.sha256(combined_string.encode("utf-8")).hexdigest()
        return anonymous_id

    def has_changed(self, fields):
        # Check if specified fields have changed.
        if not self.pk:
            return True  # New instance
        old_instance = User.objects.filter(pk=self.pk).first()
        return any(getattr(self, field) != getattr(old_instance, field) for field in fields)

    def check_password(self, raw_password):
        # Check the password.
        return check_password(raw_password, self.password)


@receiver(pre_save, sender=User)
def pre_save_user(sender, instance, **kwargs):
    """
        Generate anonymous ID and hash password before saving.
    """
    # Generate or update anonymous ID only if the email or security response changes
    if not instance.anonymous_unique_id or instance.has_changed(['email', 'security_query_response']):
        instance.anonymous_unique_id = instance.generate_anonymous_id()

    # Hash the password before saving if not already hashed
    if not instance.password.startswith("pbkdf2_"):
        instance.password = make_password(instance.password)
