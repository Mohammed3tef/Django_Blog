from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from .models import Profile


class RegistrationForm(UserCreationForm):
    username = UsernameField( widget=forms.TextInput(attrs={'class': 'input100', 'autofocus': True, 'placeholder': 'username', }),
        label="username",help_text="Required letters & digits & (@,.,-,+,_)"
        )
    email = forms.EmailField(required=True,max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'input100' ,'placeholder': 'email@example.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100','placeholder': 'Enter new password'}),
    label="password",help_text="at least 8 charachters , numbers , symbols or better mix them")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100','placeholder': 'Confirm your password'}),
    label="confirm password")
    class Meta:
        model = User
        fields =['username','email','first_name' , 'last_name' ]
        widgets = {
			'username' : forms.TextInput(attrs={'class': 'input100','placeholder': 'Enter username'}),
            'first_name':forms.TextInput(attrs={'class': 'input100' ,'placeholder': 'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class': 'input100','placeholder': 'Enter your last name'}),
		}
    def clean(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already used before.. try another one")
        return self.cleaned_data

class ProfileForm(forms.ModelForm):

    profile_pic =forms.ImageField(required=False)
    bio = forms.CharField(required = False ,widget=forms.Textarea(attrs={"rows":5, "cols":20 ,  'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ["bio",'profile_pic']

class LoginForm(AuthenticationForm): 
    username = UsernameField(
        widget=forms.TextInput(attrs={'class': 'input100', 'autofocus': True, 'placeholder': 'username'})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'password'}))

class EditProfileForm(forms.ModelForm):
    first_name =forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    class Meta:
        model = User
        fields =["first_name","last_name"]


