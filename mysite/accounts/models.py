from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_accounts")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
