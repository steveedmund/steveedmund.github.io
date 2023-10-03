from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Animal_Shelter_Model

# Register your models here.

class Animal_Shelter_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(Animal_Shelter_Model,Animal_Shelter_Admin)
