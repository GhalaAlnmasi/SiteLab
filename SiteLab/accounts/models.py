from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.user.username