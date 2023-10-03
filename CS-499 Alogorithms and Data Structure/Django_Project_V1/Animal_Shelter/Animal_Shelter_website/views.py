#************************************************************************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file contains views for a Django web application, including user authentication and registration.
#***********************************************************************************************************************#

# Importing necessary modules
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm  # Importing the SignUpForm from forms.py

# Define the 'home' view
def home(request):
    if request.method == 'POST':
        # Handling POST request when the user submits the login form
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user using the provided username and password
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # If authentication fails, display an error message and redirect to the home page
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        # Handling GET request by rendering the home.html template
        return render(request, 'home.html', {})

# Define the 'logout_user' view
def logout_user(request):
    logout(request)  # Log the user out
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')  # Redirect to the home page after logout

# Define the 'register_user' view
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # If the registration form is valid, save the new user's information
            form.save()
            
            # Authenticate and log in the newly registered user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = SignUpForm()  # Create a new registration form
        
    return render(request, 'register.html', {'form': form})  # Render the register.html template with the form
