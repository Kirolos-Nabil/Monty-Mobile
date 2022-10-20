from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "app2/home.html")


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    return render(request, "app2/dashboard.html")


@login_required(login_url='login')
def introduction(request):
    return render(request, "app2/introduction.html")


def create_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "app2/create-user.html", {
                "message": "Passwords must match.",
            })
        
        # Attempt to create new user
        try:

            validate_password(password)
            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
            user.save()
            messages.success(request, 'User Created Successfully.')

        except ValidationError as e:
            for msg in e :
                messages.error(request, msg)
                print(msg)
            return render(request, "app2/create-user.html", {
                "message": "Password is weak."
            })
        except IntegrityError:
            return render(request, "app2/create-user.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("login"))
    
    else:
        return render(request, "app2/create-user.html")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, id):
    user_id = id
    edit_user = User.objects.get(id=user_id)
    
    if request.method == "POST":
        username = request.POST["UserName"]
        email = request.POST["Email"]
        active = request.POST["Active"]
        staff = request.POST["Staff"]

        # Ensure User Email isn't exist
        if User.objects.filter(email=email) and email != edit_user.email:
            return render(request, "app2/edit_user.html", {
                "message": "User Email is already exist.",
                "id": user_id,
                "username": edit_user.username,
                "email": edit_user.email,
                "active": edit_user.is_active,
                "staff": edit_user.is_staff,
            })

        # Attempt to Edit User
        try:
            edit_user.username = username
            edit_user.email = email
            edit_user.is_active = active
            edit_user.is_staff = staff
            edit_user.save()
            messages.success(request, 'User Edited Successfully.')
        except IntegrityError:
            return render(request, "app2/edit_user.html", {
                "message": "edit_user_error.",
                "id": user_id,
                "username": edit_user.username,
                "email": edit_user.email,
                "active": edit_user.is_active,
                "staff": edit_user.is_staff,
            })
        return HttpResponseRedirect(reverse("app2:users"))
    return render(request, "app2/edit_user.html", {
        "id": user_id,
        "username": edit_user.username,
        "email": edit_user.email,
        "active": edit_user.is_active,
        "staff": edit_user.is_staff,
    } )



@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def users(request):
    user_results = User.objects.filter(is_superuser=False)
    return render(request, "app2/users.html" , {"Users": user_results} )


@login_required(login_url='login')
def change_password(request):
   form = PasswordChangeForm(user=request.user, data=request.POST)
   if form.is_valid():
     form.save()
     messages.success(request, 'Password Changed Successfully')
     update_session_auth_hash(request, form.user)
     logout(request)
     return redirect('/')
   return render(request, 'app2/change_password.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("app2:home"))