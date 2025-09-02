from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def profile_picture_remove(request):
    profile = request.user.profile
    if profile.profile_picture:
        # Don't delete the file, just remove the reference
        profile.profile_picture.delete(save=False)
        profile.profile_picture = None
        profile.save()
        messages.success(request, 'Profile picture removed successfully!')
    return redirect('profile_edit')