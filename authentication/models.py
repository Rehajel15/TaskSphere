from django.db import models
from django.contrib.auth.models import User
from home.models import Group

# Create your models here.

class ExtendedUserInformation(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, editable=False)
    biography = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/")
    in_group = models.OneToOneField(Group, null=True, blank=True, on_delete=models.CASCADE)  # Function in signals.py for removing the users

    def __str__(self):
        return str(self.user.username)
