from .models import Profile
from Dj_blog.settings import BASE_DIR
import os
from manager.logger import log

def demote_user(user):
    user.is_staff = False
    user.save()
