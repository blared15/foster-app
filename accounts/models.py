from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.utils import timezone

def profile_picture_upload_path(instance, filename):
    # Generate path for profile pictures: media/profile_pictures/user_id/filename
    ext = filename.split('.')[-1]
    filename = f"{instance.user.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('profile_pictures', str(instance.user.id), filename)

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('guest', 'Guest'),
        ('foster', 'Foster'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=profile_picture_upload_path,
        blank=True,
        null=True,
        default='profile_pictures/default.png'
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='foster')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
    
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default-profile.png'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()