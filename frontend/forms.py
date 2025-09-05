from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    number = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your phone number"
    )

    class Meta:
        model = CustomUser   # ✅ use your custom user model
        fields = ['username', 'email', 'password1', 'password2', 'number']  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.number = self.cleaned_data['number']  # ✅ only if CustomUser has `number` field
        if commit:
            user.save()
        return user
