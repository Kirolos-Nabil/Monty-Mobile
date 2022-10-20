from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect(reverse("app2:home"))
        else:
            print("kkkkkkkkkkkk")
        
    
    elif request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("app2:home"))
        else:
            return render(request, "assignments/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "assignments/login.html")


