#*******************************************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This file represents a Django migration that creates the 'Shelter_data' model.
#*******************************************************************************************#

# Importing necessary modules from Django
from django.db import migrations, models

# Defining a migration class
class Migration(migrations.Migration):
    # Setting the initial migration state
    initial = True

    # Specifying dependencies, if any (in this case, there are no dependencies)
    dependencies = [
    ]

    # Defining migration operations
    operations = [
        # Creating the 'Shelter_data' model with its fields
        migrations.CreateModel(
            name='Shelter_data',  # Name of the model
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # Auto-generated primary key field
                ('created_at', models.DateTimeField(auto_now_add=True)),  # Date and time when the record was created
                ('age_upon_outcome', models.CharField(max_length=50)),  # Field for age upon outcome
                ('animal_id', models.CharField(max_length=50)),  # Field for animal ID
                ('animal_type', models.CharField(max_length=500)),  # Field for animal type
                ('breed', models.CharField(max_length=50)),  # Field for breed
                ('color', models.CharField(max_length=50)),  # Field for color
                ('date_of_birth', models.CharField(max_length=50)),  # Field for date of birth
                ('datetime', models.CharField(max_length=50)),  # Field for datetime
                ('monthyear', models.CharField(max_length=50)),  # Field for monthyear
                ('name', models.CharField(max_length=50)),  # Field for name
                ('outcome_subtype', models.CharField(max_length=50)),  # Field for outcome subtype
                ('outcome_type', models.CharField(max_length=50)),  # Field for outcome type
                ('sex_upon_outcome', models.CharField(max_length=50)),  # Field for sex upon outcome
                ('location_lat', models.CharField(max_length=50)),  # Field for location latitude
                ('location_long', models.CharField(max_length=50)),  # Field for location longitude
                ('age_upon_outcome_in_weeks', models.CharField(max_length=50)),  # Field for age upon outcome in weeks
            ],
        ),
    ]
