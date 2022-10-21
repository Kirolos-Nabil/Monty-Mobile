from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    return render(request, "app1/users.html" )