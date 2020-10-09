from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
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
            form.save()
            return redirect('/flights')
    return render(request,'flights/add_flight.html',{'form':form})

        

    
    
