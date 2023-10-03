#*****************************************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file registers the 'Shelter_data' model with the Django admin panel.
#*****************************************************************************************#

# Importing the admin module from django.contrib
from django.contrib import admin
# Importing the 'Shelter_data' model from the same directory
from .models import Shelter_data

# Registering the 'Shelter_data' model with the Django admin panel
admin.site.register(Shelter_data)
