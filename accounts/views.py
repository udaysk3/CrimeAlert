# views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import PoliceSignupForm
from .forms import PoliceLoginForm
from .models import Police, User
from home.models import ScamReport

def police_signup(request):
    if request.method == 'POST':
        form = PoliceSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/user/police/login')  
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
            request.session["user"] = str(user)
            request.session["district"] = str(user.district)
            scams = list(ScamReport.objects.filter(district=user.district).values())
            for scam in scams:
                scam["user"] = User.objects.get(id=scam["user_id"]).username
            request.session["scams"] = scams
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

def change_district(request):
    if request.method=="POST":
        if request.POST.get("police"):
            police = Police.objects.filter(station_code = request.POST['police']).update(district=request.POST["district"])
            request.session["district"] = request.POST["district"]
        else:
            user = User.objects.filter(username = request.POST['citizen']).update(district = request.POST["district"])
        return redirect("/")