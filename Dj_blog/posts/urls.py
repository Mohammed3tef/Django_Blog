from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts),
    path('createpost', views.post_create),
    path('updatepost/<id>', views.post_update),
]
