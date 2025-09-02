from django.db import models
from accounts.models import Profile

class Contact(models.Model):
    CONTACT_TYPE_CHOICES = (
        ('family', 'Family'),
        ('medical', 'Medical'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    )
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPE_CHOICES, default='other')
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15,blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.relationship}"