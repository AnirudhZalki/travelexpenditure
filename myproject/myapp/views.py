from django.shortcuts import render
from .models import VehicleTrip, Journey
import requests
from django.http import JsonResponse
from django.conf import settings
import os
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def contact_submit(request):
    if request.method == 'POST':
        # Process form data here (e.g., send email or store in DB)
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        # Do something with this info
        return render(request, 'contact.html', {'success': True})


def past_journeys(request):
    journeys = Journey.objects.all().order_by('-journey_date')
    return render(request, 'journeys.html', {'journeys': journeys})


def vehicle_expense(request):
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        distance = float(request.POST.get("distance"))
        tolls = int(request.POST.get("tolls"))

        fuel_rate = 105  # ₹ per liter
        mileage = 18     # km per liter
        fuel_cost = round((distance / mileage) * fuel_rate, 2)
        toll_cost = tolls * 60
        total_cost = fuel_cost + toll_cost

        # Save to database
        Journey.objects.create(
            source=source,
            destination=destination,
            distance_km=distance,
            toll_gates=tolls,
            fuel_cost=fuel_cost,
            toll_cost=toll_cost,
            total_cost=total_cost,
            journey_date=datetime.now()
        )

        result = {
            "source": source,
            "destination": destination,
            "fuel_cost": fuel_cost,
            "toll_charges": toll_cost,
            "total": total_cost
        }

        return render(request, "vehicle_form.html", {"result": result})

    return render(request, "vehicle_form.html")


def get_toll_data(request):
    try:
        lat1 = float(request.GET.get('lat1'))
        lon1 = float(request.GET.get('lon1'))
        lat2 = float(request.GET.get('lat2'))
        lon2 = float(request.GET.get('lon2'))

        # Use Haversine formula to calculate the distance between the two coordinates
        R = 6371  # Earth radius in km
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)

        a = sin(dLat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        # Here, you would calculate the number of toll gates based on the distance or some external API
        tolls = int(distance // 50)  # Example: one toll gate every 50 km

        # You can fetch actual toll data from an API like TollGuru (adjust based on API)
        api_key = os.getenv("TOLLGURU_API_KEY")
        url = f'https://api.tollguru.com/v1/calculate'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }
        params = {
            'start_lat': lat1,
            'start_lon': lon1,
            'end_lat': lat2,
            'end_lon': lon2,
        }
        response = requests.get(url, headers=headers, params=params)
        toll_data = response.json()

        toll_tag_cost = toll_data.get('toll_tag_cost', 0)  # Assume `toll_tag_cost` comes from API

        return JsonResponse({
            'tolls': tolls,
            'toll_tag_cost': toll_tag_cost,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)