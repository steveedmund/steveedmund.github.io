#***********************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file defines URL patterns for a Django web application.
#***********************************************************************#

# Importing necessary modules
from django.urls import path
from . import views  # Importing views from the same directory

# Define URL patterns for the application
urlpatterns = [
    path('', views.home, name='home'),  # Route for the home page, calls the 'home' function in views.py
    # path('login/', views.login_user, name='login'),  # Route for user login (commented out)
    path('logout/', views.logout_user, name='logout'),  # Route for user logout, calls 'logout_user' function in views.py
    path('register/', views.register_user, name='register'),  # Route for user registration, calls 'register_user' function in views.py
]
