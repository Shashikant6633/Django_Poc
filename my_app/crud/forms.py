from django import forms
from .models import Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'description', 'author', 'price', 'isbn', 'image']

class RegistrationForm(UserCreationForm):
    # Add any additional fields if needed
 
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
 
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 == password2:
    #         return password2
    #     raise forms.ValidationError("Passwords do not match or are too similar to the username.")
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password2'].validators = []  # Remove the password similarity validator
 
        def clean_password1(self):
            password1 = super().clean_password1()
 
        # Run the default password validators manually
            errors = []
            for validator in password_validation.get_default_password_validators():
                try:
                     validator.validate(password1, self.instance)
                except forms.ValidationError as error:
                    errors.append(error)
 
        # Check if the password contains a substring of the username
            username = self.cleaned_data.get('username')
            if username and username.lower() in password1.lower():
                errors.append(forms.ValidationError(
                    ("The password cannot contain a substring of the username."),
                    code='password_too_similar'
                ))
 
            if errors:
                raise forms.ValidationError(errors)
 
            return password1

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']