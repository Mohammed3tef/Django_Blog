
from Dj_blog.settings import BASE_DIR
import os

def isLocked(user):
    return user.profile.is_locked

def delete_profile_pic(profile_pic):
    try:
        pic_url = BASE_DIR+profile_pic.url
        if(pic_url.endswith("defaultAvatare.png")):
            pass
        else:
            os.remove(pic_url)
    except Exception as ex:
        print('error')
