#***************************************************************************#
#Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file defines a custom registration form for user sign-up.
#**************************************************************************#

# Importing necessary modules
from django.contrib.auth.forms import UserCreationForm  # Importing UserCreationForm for basic user registration
from django.contrib.auth.models import User  # Importing User model
from django import forms  # Importing forms module for creating form fields

# Define a custom registration form by extending UserCreationForm
class SignUpForm(UserCreationForm):
    # Adding additional fields to the form

    # Email field with custom widget and placeholder
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    # First Name field with custom widget and placeholder
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))

    # Last Name field with custom widget and placeholder
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    # Company Name field with custom widget and placeholder
    company_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Company'}))

    class Meta:
        model = User  # Specify the User model
        # Specifying the fields to be included in the form
        fields = ('username', 'first_name', 'last_name', 'company_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Customizing widget attributes for the 'username' field
        self.fields['username'].widget.attrs['class'] = 'form-control'  # Adding a CSS class
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'  # Adding a placeholder
        self.fields['username'].label = ''  # Removing the label
        # Adding help text for the 'username' field
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        # Customizing widget attributes for the 'password1' field
        self.fields['password1'].widget.attrs['class'] = 'form-control'  # Adding a CSS class
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'  # Adding a placeholder
        self.fields['password1'].label = ''  # Removing the label
        # Adding help text for the 'password1' field
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        # Customizing widget attributes for the 'password2' field
        self.fields['password2'].widget.attrs['class'] = 'form-control'  # Adding a CSS class
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'  # Adding a placeholder
        self.fields['password2'].label = ''  # Removing the label
        # Adding help text for the 'password2' field
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
