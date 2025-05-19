from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    # Add other profile-related fields here

    def __str__(self):
        return self.user.username
