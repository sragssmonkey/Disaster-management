from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    number = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your phone number"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # keep only User fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # number is not part of User → you can store it in a Profile model or handle it separately
        if commit:
            user.save()
        return user
