from .models import Profile
from Dj_blog.settings import BASE_DIR
from users.logger import log

def isLocked(user):
    return user.profile.is_locked

def demote_user(user):
    user.is_staff = False
    user.save()

def lock_user(user):
    profile = Profile.objects.get(user=user)
    profile.is_locked = True
    profile.save()

def unlock_user(user):
    profile = Profile.objects.get(user=user)
    profile.is_locked = False
    profile.save()