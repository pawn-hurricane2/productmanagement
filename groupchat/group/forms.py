import datetime

from django import forms
from .models import RegisteredUsers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)))
    cell_phone = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=10, render_value=False)))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=10, render_value=False)))

    def clean_cell_phone(self):
        phone_number_given = self.cleaned_data["cell_phone"]
        if phone_number_given:
            if not phone_number_given.isdigit():
                raise forms.ValidationError("Please don't enter any character in cell phone section")

            if len(phone_number_given) != 10:
                raise forms.ValidationError("Entered phone number must be of 10 digits")

            return self.cleaned_data["cell_phone"]

    def clean(self):
        if not self._errors:
            user_with_same_email = RegisteredUsers.objects.filter(email=self.cleaned_data["email"])
            if user_with_same_email:
                raise forms.ValidationError(
                    "Oops!!! A user with this email already exists. Please provide another email")

            if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
                raise forms.ValidationError("Password and Confirm Password do not match")

        return self.cleaned_data

    def save(self):
        self.cleaned_data.pop("confirm_password")
        password = self.cleaned_data["password"]
        hashed_password = make_password(password=password)
        self.cleaned_data["password"] = hashed_password
        user_registration_data = self.cleaned_data
        RegisteredUsers.objects.create(**user_registration_data)



class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=10, render_value=False)))

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean(self):
        if not self._errors:
            email = self.cleaned_data["email"].lower()
            password = self.cleaned_data["password"]

            self.user = authenticate(username=email, password=password)
            if not self.user:
                is_registered_user = True if RegisteredUsers.objects.filter(email=email) else False
                if is_registered_user:
                    raise forms.ValidationError("Email Id and Password did not match")
                else:
                    raise forms.ValidationError("This Email Id is not registered")

        return self.cleaned_data

    def get_authenticated_user(self):
        return self.user
