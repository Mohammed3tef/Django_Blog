from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, ProfileForm, LoginForm
from .models import Profile
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .util_funcs import isLocked


import logging
# Create your views here.

# Register view
def register(request):

    if(not request.user.is_authenticated):
        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            profile_form = ProfileForm(request.POST, request.FILES)

            if user_form.is_valid():
                user = user_form.save()  # save the user into database and return it

                profile = Profile.objects.get(user=user)
                file = request.FILES.get("profile_pic")
                if(file != None):
                    profile.profile_pic = file  # add the provided pic to that user profile
                profile.bio = request.POST["bio"]
                profile.save()  # save the updates to user profile

                logging.info("Saved profile")

                user = authenticate(
                    username=request.POST["username"], password=request.POST["password1"])
                if user is not None:
                    login(request, user)
                    try:
                        send_mail('Welcome to our blog', 'Django Blog team welcomes you to our blog .',
                                  'iti42@itians.com', [user.email], fail_silently=False,)
                    except Exception as ex:
                        logging.info("couldn't send email message"+str(ex))

                    # redirect to user profile page
                    # return HttpResponseRedirect("/users/profile")
                else:
                    logging.info("cannot login from refistration form")
            else:
                logging.info("invalid registration form")  # for debugging purposes
        else:
            user_form = RegistrationForm()
            profile_form = ProfileForm()
        context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, 'users/register.html', context)
    else:
        return HttpResponseRedirect("/")

def login_view(request):

    # check if user is already logged in
    if(not request.user.is_authenticated):
        if request.method == "POST":

            login_form = LoginForm(data=request.POST)
            if(login_form.is_valid()):
                username = request.POST['username']
                password = request.POST["password"]

                user = authenticate(username=username, password=password)
                if user is not None:  # user authenticated
                    if(isLocked(user)):
                        log(user.username + " blocked user")
                        # blocked users Page
                        return HttpResponseRedirect("/users/blocked")
                    else:
                        login(request, user)
                        logging.info(user.username + " logged in successfully")
                        # homepage
                        return HttpResponseRedirect("/")
                else:
                    logging.info("cannot login from login page")
            else:
                logging.info("invalid login form")
        else:
            login_form = LoginForm()
        context = {"login_form": login_form}
        return render(request, 'users/login.html', context)
    else:
        return HttpResponseRedirect("/users/profile")

def blocked(request):
    # Go to login, You are not allowed to access this page
    if(not request.user.is_authenticated):
        admins = User.objects.all().filter(is_staff__exact=True)
        return render(request, "users/blocked.html", {"admins": admins})
    return HttpResponseRedirect("/")

def profile(request):
    if(request.user.is_authenticated):
        user = request.user  # get the current user
        # get the profile related to that user
        userprofile = Profile.objects.get(user=user)
        context = {"user": user, "userprofile": userprofile}
        return render(request, "users/profile.html", context)
    else:
        return HttpResponseRedirect("/")

