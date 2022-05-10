from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
        
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