from django.urls import path
from . import views


#the part of urls begins with users/ or admins/ is to handle all crud operations on users and admins 

urlpatterns = [
path("users/", views.users, name="users"),
path("users/lock/<int:id>/", views.lock, name="lock"),

]