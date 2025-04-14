from django.shortcuts import render

from .models import VehicleTrip, Journey


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
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        distance = float(request.POST.get("distance"))
        tolls = int(request.POST.get("tolls"))

        fuel_price_per_km = 5
        toll_charge_per_gate = 100

        fuel_cost = distance * fuel_price_per_km
        toll_charges = tolls * toll_charge_per_gate
        total = fuel_cost + toll_charges

        # Save to database
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
# Create your views here.
