from .models import Profile
from Dj_blog.settings import BASE_DIR
import logging
import os

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

    
def delete_profile_pic(profile_pic):
    try:
        pic_url = BASE_DIR+profile_pic.url
        if(pic_url.endswith("image_1.jpg")):
            pass
        else:
            os.remove(pic_url)
            logging.info("profile pic has been deleted")
    except Exception as ex:
        logging.info("no pic"+str(ex))

def promote_to_staff(user):
    """this function can be used to promot a normal user to be a staff user with the required permissions"""
    user.is_staff = True
    user.save()

def promote_to_super_user(user):
    promote_to_staff(user)
    user.is_superuser = True
    user.save()
