from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import flight_form,passenger_form

from flights.models import Flight,Passengers
# Create your views here.
def index(request):
    return render(request,"flights/index.html",{
        "flights":Flight.objects.all()
    })
    
def flight(request, flightid):
    flight=Flight.objects.get(id=flightid)    
    passengers=Passengers.objects.all()
    form=passenger_form()
    if request.method=="POST":
        form=passenger_form(request.POST)
        passenger_form.clean_first()
        return render(request, "flights/flight.html", {
            "form":form,
            "flight": flight,
            "passengers": flight.passengers.all(),
            "non_passengers": passengers.exclude(flight=flight),
        })
        
        
    return render(request,"flights/flight.html",{
        "form":form,
        "flight":flight,
        "passengers":flight.passengers.all(),
        "non_passengers":passengers.exclude(flight=flight),
    })
    
def book(request,flightid):
    if request.method=="POST":
        x=request.POST.get('passengerid')
        flight=Flight.objects.get(id=flightid)
        passenger=Passengers.objects.get(id=x)
        print("FLIGHT: ",flight)
        print("PASSENGER: ",passenger)
        passenger.flight.add(flight)        
        print("THE ID OF PASSENGER is: ",x)
        return HttpResponseRedirect(reverse('flight',args=(flightid,)))
    
def add_flight(request):
    form=flight_form()
    if request.method=="POST":
        form=flight_form(request.POST)
        if form.is_valid():
            origin=request.POST.get('origin')
            destination=request.POST.get('destination')
            x=Flight.objects.filter(origin=origin,destination=destination)
            if len(x)==0:
                form.save()
                messages.success(request,"THE FLIGHT IS SUCCESSFULLY ADDED")
                return redirect('/flights')
            else:
                messages.error(request,'THE FLIGHT ALREADY EXISTS')

    return render(request,'flights/add_flight.html',{'form':form})

def add_passenger(request,flightid):
    form=passenger_form(request.POST)
    flight=Flight.objects.get(id=flightid)
    flightid=request.POST.get('flightid')
    first=request.POST.get('first')
    last=request.POST.get('last')
    x=Passengers.objects.filter(first=first,last=last)
    if len(x)>0:
        messages.error(request,'The Passenger is Already in the List')
        return HttpResponseRedirect(reverse('flight',args=flightid,))
    else:
        passenger=Passengers.objects.create(first=first,last=last)
        passenger.flight.add(flight)
        return HttpResponseRedirect(reverse('flight',args=flightid,))
        
def delete_passenger(request,flightid):
    passenger_id=request.POST.get('passenger_id')
    flight=Flight.objects.get(id=flightid)
    passenger=Passengers.objects.get(id=passenger_id)
    passenger.flight.remove(flight)
    return redirect(f'/flights/{flightid}')
                

        

    
    
