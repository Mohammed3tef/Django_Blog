from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.models import Profile
from django.contrib.auth.models import User
from users.logger import log
from users.util_funcs import *
from django.core.paginator import Paginator
import os

""" the following functions are to control users or admins
    providing some functionality to be used in views
"""

def manager_show_normal_users(request):
    """ show all normal users [not admins nor super users]
    @params : request """

    if(is_authorized_admin(request)):
        users = User.objects.filter(is_staff__exact=False)
        paginator = Paginator(users, 5)
        page_number = request.GET.get('page')
        page_users = paginator.get_page(page_number)
        return render(request, "manager/users.html", {"users": page_users})
    else:
        return HttpResponseRedirect("/")

def manager_lock_user(request, id):
    """ lock a specific user not to be able to login again but his account is still alive
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        lock_user(user)
        log(request.user.username+" locked " + user.username+".")
        return HttpResponseRedirect("/manager/users")
    else:
        return HttpResponseRedirect("/")

def manager_unlock_user(request, id):
    """ unlock a specific user and becomes able to login again
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        unlock_user(user)
        log(request.user.username+" unlocked " + user.username+".")
        return HttpResponseRedirect("/manager/users")
    else:
        return HttpResponseRedirect("/")

def manager_delete_user(request, id):
    """ delete a specific user not to be able to login and his account is deleted
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        if(user.profile.profile_pic != None):
            delete_profile_pic(user.profile.profile_pic)
        user.delete()
        log(request.user.username+" removed " + user.username+".")
        return HttpResponseRedirect("/manager/users")
    else:
        return HttpResponseRedirect("/")

def manager_show_user(request, id):
    """ show info of specific user all his profile with some additional info only revealed for admins
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        return render(request, "manager/show_user.html", {"user": user})
    else:
        return HttpResponseRedirect("/")

def manager_show_admins(request):
    """ show all admin users [admins or super users]
    @params : request """

    if(is_authorized_admin(request)):
        admins = User.objects.filter(is_staff__exact=True)
        paginator = Paginator(admins, 5)
        page_number = request.GET.get('page')
        page_admins = paginator.get_page(page_number)
        context = {"admins": page_admins,"superuser": request.user.is_superuser}
        return render(request, "manager/admins.html", context)
    else:
        return HttpResponseRedirect("/")





def is_authorized_admin(request):
    if(request.user.is_authenticated):
        if(request.user.is_staff):
            return True
    return False
