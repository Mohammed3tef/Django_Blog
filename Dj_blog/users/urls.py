from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register , name='register'),
    path('login/',views.login_view , name='login'),

    path('blocked/',views.blocked,name="blocked"),
    path("profile/",views.profile , name="profile"),

]
