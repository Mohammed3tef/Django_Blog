from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

fs = FileSystemStorage()


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        verbose_name="profile picture", storage=fs, default='defaultAvatar.png')
    undesired_words_count = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    bio = models.TextField(max_length=200, default="")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
