from django.shortcuts import render

from .models import VehicleTrip, Journey
import requests
from django.http import JsonResponse

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

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
    result = None
    if request.method == "POST":
        source = request.POST.get("source")  # coordinates as string e.g. "12.97,77.59"
        destination = request.POST.get("destination")
        distance = float(request.POST.get("distance"))
        tolls = int(request.POST.get("tolls"))

        fuel_price_per_km = 5
        toll_charge_per_gate = 100

        fuel_cost = distance * fuel_price_per_km
        toll_charges = tolls * toll_charge_per_gate
        total = fuel_cost + toll_charges

        # Save to Journey model
        Journey.objects.create(
            source=source,
            destination=destination,
            distance_km=distance,
            toll_gates=tolls,
            fuel_cost=fuel_cost,
            toll_cost=toll_charges,
            total_cost=total
        )

        result = {
            'source': source,
            'destination': destination,
            'fuel_cost': fuel_cost,
            'toll_charges': toll_charges,
            'total': total
        }

    return render(request, 'vehicle_form.html', {'result': result})


def get_toll_data(request):
    lat1 = request.GET.get('lat1')
    lon1 = request.GET.get('lon1')
    lat2 = request.GET.get('lat2')
    lon2 = request.GET.get('lon2')

    if not all([lat1, lon1, lat2, lon2]):
        return JsonResponse({'error': 'Missing coordinates'}, status=400)

    API_KEY = '7f517bd02b1e4a5dd09cb4dc0faf17e9'  # Replace this with your actual key

    url = f"https://apis.mapmyindia.com/advancedmaps/v1/{API_KEY}/route_adv/toll?start={lat1},{lon1}&end={lat2},{lon2}&rtype=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tolls = data.get("toll_count", 0)
        return JsonResponse({'tolls': tolls})
    else:
        return JsonResponse({'tolls': 0})