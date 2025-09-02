from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    context = {
        'user_profile': request.user.profile,
    }
    return render(request, 'core/dashboard.html', context)

def admin_required(user):
    return user.is_authenticated and user.profile.role == 'admin'

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')