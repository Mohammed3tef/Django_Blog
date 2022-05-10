from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, ProfileForm
from .models import Profile
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
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
