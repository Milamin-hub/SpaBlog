from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='profile_photos', default='profile_photos/no_user.png')

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.user.username
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

