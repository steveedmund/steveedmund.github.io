#***********************************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file configures the Django application 'Animal_Shelter_website'.
#***********************************************************************************#

# Importing the AppConfig class from django.apps
from django.apps import AppConfig

# Creating a configuration class for the 'Animal_Shelter_website' app
class AnimalShelterWebsiteConfig(AppConfig):
    # Setting the default auto field for database models
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Setting the name of the app
    name = 'Animal_Shelter_website'
