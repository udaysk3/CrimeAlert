# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import PoliceSignupForm
from .forms import PoliceLoginForm
from .models import Police


def police_signup(request):
    if request.method == 'POST':
        form = PoliceSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')  
    else:
        form = PoliceSignupForm()

    return render(request, 'account/police_signup.html', {'form': form})


def police_login(request):
    if request.method == 'POST':
        form = PoliceLoginForm(request, request.POST)
        station_code = request.POST['station_code']
        password = request.POST['password']
        user = Police.objects.get(station_code=station_code, password= password)
        if user is not None:
            request.session["user"] = f"Police-{station_code}"
            return redirect('/')  
    else:
        form = PoliceLoginForm()

    return render(request, 'account/police_signin.html', {'form': form})

def police_logout(request):
    try:
        del request.session["user"]
        return redirect("/")
    except:
        print("Something went wrong")