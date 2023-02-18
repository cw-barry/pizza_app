from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class RegistrationForm(UserCreationForm):
    # email = forms.EmailField()
    class Meta:
        model = User
        fields= ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is mandatory!")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is allready inuse. Please choose different email!")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ['address', 'phone', 'image']
        exclude = ['user']
