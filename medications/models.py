from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

class Medication(models.Model):
    FREQUENCY_CHOICES = (
        ('once_daily', 'Once Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times', 'Three Times Daily'),
        ('four_times', 'Four Times Daily'),
        ('as_needed', 'As Needed'),
    )
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True)
    prescribing_doctor = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.profile.user.get_full_name()}"

class MedicationAdministration(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('administered', 'Administered'),
        ('missed', 'Missed'),
        ('refused', 'Refused'),
    )
    
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='administrations')
    scheduled_time = models.DateTimeField()
    administered_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    administered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication.name} - {self.scheduled_time}"