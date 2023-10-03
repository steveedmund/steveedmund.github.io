#****************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file defines a Django model for shelter data.
#***************************************************************#

# Importing the necessary module for Django models
from django.db import models

# Defining a Django model for shelter data
class Shelter_data(models.Model):
    # Automatically add the creation timestamp when a record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields for various attributes of shelter data
    age_upon_outcome = models.CharField(max_length=50)  # Age upon outcome
    animal_id = models.CharField(max_length=50)  # Unique animal ID
    animal_type = models.CharField(max_length=500)  # Type of animal
    breed = models.CharField(max_length=50)  # Breed of the animal
    color = models.CharField(max_length=50)  # Color of the animal
    date_of_birth = models.CharField(max_length=50)  # Date of birth of the animal
    datetime = models.CharField(max_length=50)  # Datetime information
    monthyear = models.CharField(max_length=50)  # Month and year information
    name = models.CharField(max_length=50)  # Name of the animal
    outcome_subtype = models.CharField(max_length=50)  # Outcome subtype
    outcome_type = models.CharField(max_length=50)  # Outcome type
    sex_upon_outcome = models.CharField(max_length=50)  # Sex upon outcome
    location_lat = models.CharField(max_length=50)  # Latitude information
    location_long = models.CharField(max_length=50)  # Longitude information
    age_upon_outcome_in_weeks = models.CharField(max_length=50)  # Age upon outcome in weeks

    # A human-readable representation of the object
    def __str__(self):
        # Construct a human-readable string for this object
        return f"{self.age_upon_outcome} {self.animal_id} {self.animal_type} {self.breed} {self.color} {self.date_of_birth} {self.datetime} {self.monthyear} {self.name} {self.outcome_subtype} {self.outcome_type} {self.sex_upon_outcome} {self.location_lat} {self.location_long} {self.age_upon_outcome_in_weeks}"
