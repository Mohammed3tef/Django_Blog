from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/',views.register , name='register'),
    path('login/',views.login_view , name='login'),

    path('blocked/',views.blocked,name="blocked"),
    path("profile/",views.profile , name="profile"),
    path('logout/',auth_views.LogoutView.as_view(template_name="users/logout.html"),name='logout'),

]
