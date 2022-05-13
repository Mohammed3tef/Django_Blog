from django.shortcuts import render
from .crud_users import *
from posts.models import Post, Tag, Category, Comment, Profanity
from posts.forms import PostForm, CommentForm, ProfanityForm, CategoryForm

# the following views are to control users and admins 
def users(request):
    return manager_show_normal_users(request)

def lock(request, id):
    return manager_lock_user(request, id)


def unlock(request, id):
    return manager_unlock_user(request, id)

def delete(request, id):
    return manager_delete_user(request, id)

def show(request, id):
    return manager_show_user(request, id)

def admins(request):
    return manager_show_admins(request)

def demote(request, id):
    return super_demote_admin(request, id)

def lock_admin(request, id):
    return super_lock_admin(request, id)

def unlock_admin(request, id):
    return super_unlock_admin(request, id)
