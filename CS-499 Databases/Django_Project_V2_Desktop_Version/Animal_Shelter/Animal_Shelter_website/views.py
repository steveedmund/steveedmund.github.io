from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Animal_Shelter_Model
from django.db.models import Count
import json
import folium

def home(request):
    #shelter_model = Animal_Shelter_Model.objects.all()

    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Logged In!")
                return redirect('data_table')
            else:
                messages.success(request, "There Was An Error Logging In, Please Try Again...")
                return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


def data_table(request):
    if request.method == 'POST':
        # Check which checkboxes were selected
        #filter_water_rescue = request.POST.get('filter_water_rescue')
        #filter_mountain_rescue = request.POST.get('filter_mountain_rescue')
        #filter_disaster_rescue = request.POST.get('filter_disaster_rescue')
        #filter_reset = request.POST.get('filter_reset')
        filter_type = request.POST.get('filter_type')
        # Initialize a queryset with all data
        filtered_data = Animal_Shelter_Model.objects.all()
        
        # Apply filters based on selected checkboxes
        if filter_type == "water_rescue":
            filtered_data = filtered_data.filter(breed__in=['Labrador Retriever Mix', 'Labrador Retriever/Australian Cattle Dog', 'Border Collie/Queensland Heeler', 'Australian Cattle Dog Mix', 'Flat Coat Retriever Mix'])
        elif filter_type == "mountain_rescue":
            filtered_data = filtered_data.filter(breed__in=['Siberian Husky Mix', 'German Shepherd/Labrador Retriever', 'Yorkshire Terrier/Yorkshire Terrier', 'Akita Mix', 'American Eskimo/Alaskan Husky', 'Alaskan Malamute/Labrador Retriever', 'American Eskimo', 'Alaskan Husky', 'Alaskan Husky Mix'])
        elif filter_type == "disaster_rescue":
            filtered_data = filtered_data.filter(breed__in=['Beagle Mix', 'German Shepherd Mix', 'Beagle', 'Australian Shepherd Mix', 'Rottweiler/Labrador Retriever', 'Australian Shepherd Mix', 'Australian Cattle Dog/German Shepherd', 'Australian Cattle Dog/German Shorthair Pointer', 'Rottweiler', 'Beagle Mix', 'Basset Hound Mix', 'Doberman Pinsch Mix', 'Black/Tan Hound Mix', 'English Foxhound', 'Black/Tan Hound Mix', 'Anatol Shepherd'])
        elif filter_type == "reset":
            # Reset filter, show all data
            filtered_data = Animal_Shelter_Model.objects.all()
        else:
            filtered_data = Animal_Shelter_Model.objects.all()
        # Calculate the percentage of each breed type in the filtered data
        breed_counts = {}
        total_count = filtered_data.count()
        for animal in filtered_data:
            breed = animal.breed
            breed_counts[breed] = breed_counts.get(breed, 0) + 1
        
        breed_percentages = {breed: (count / total_count) * 100 for breed, count in breed_counts.items()}
        
        # Convert breed percentages data to JSON for JavaScript
        breed_percentages_json = json.dumps(breed_percentages)
        
        return render(request, 'data_table.html', {'filtered_data': filtered_data, 'breed_percentages_json': breed_percentages_json})
    else:
        # Handle GET request, show initial unfiltered data
        unfiltered_data = Animal_Shelter_Model.objects.all()
        return render(request, 'data_table.html', {'filtered_data': unfiltered_data})



def your_view(request):
    # Create a Folium map object
    my_map = folium.Map(location=[51.505, -0.09], zoom_start=5)

    # Add markers, polygons, or other map features as needed
    # For example:
    #folium.Marker([51.5, -0.1], tooltip='Marker 1').add_to(my_map)
    #folium.Marker([51.6, -0.2], tooltip='Marker 2').add_to(my_map)

    # Pass the map object to the template context
    context = {
        'my_map': my_map._repr_html_()
    }

    return render(request, 'data_table.html', context)