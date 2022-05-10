from django.shortcuts import render
from .crud_users import *
from posts.models import Post, Tag, Category, Comment, Profanity
from posts.forms import PostForm, CommentForm, ProfanityForm, CategoryForm

# the following views are to control users and admins 
def users(request):
    return manager_show_normal_users(request)
