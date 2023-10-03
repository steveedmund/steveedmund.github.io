from django.db import models

# Define the Animal_Shelter_Model class which represents your database table
class Animal_Shelter_Model(models.Model):
    # Auto-generate a 'created_at' timestamp whenever a new record is added
    created_at = models.DateTimeField(auto_now_add=True)

    # Define the 'id' field as an AutoField for primary key
    id = models.AutoField(primary_key=True)

    # Define various fields to store data about animals
    age_upon_outcome = models.CharField(max_length=50)
    animal_id = models.CharField(max_length=50)
    animal_type = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    datetime = models.DateTimeField()
    monthyear = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    outcome_subtype = models.CharField(max_length=50)
    outcome_type = models.CharField(max_length=50)
    sex_upon_outcome = models.CharField(max_length=50)
    location_lat = models.DecimalField(max_digits=10, decimal_places=8)
    location_long = models.DecimalField(max_digits=11, decimal_places=8)
    age_upon_outcome_in_weeks = models.DecimalField(max_digits=10, decimal_places=1)

    # Define a __str__ method to return a string representation of the object
    def __str__(self):
        return (
            f"{self.age_upon_outcome} {self.animal_id} {self.animal_type} {self.breed} {self.color} {self.date_of_birth} {self.datetime} {self.monthyear} {self.name} {self.outcome_subtype} {self.outcome_type} {self.sex_upon_outcome} {self.location_lat} {self.location_long} {self.age_upon_outcome_in_weeks}"
        )
