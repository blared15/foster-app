from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

class IncidentReport(models.Model):
    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    INCIDENT_TYPES = (
        ('medication', 'Medication Error'),
        ('fall', 'Fall'),
        ('behavioral', 'Behavioral Incident'),
        ('medical', 'Medical Emergency'),
        ('environmental', 'Environmental Hazard'),
        ('other', 'Other'),
    )
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='incidents')
    title = models.CharField(max_length=200)
    description = models.TextField()
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES, default='other')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    incident_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_incidents')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='assigned_incidents')
    follow_up_required = models.BooleanField(default=False)
    follow_up_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-incident_date']
    
    def __str__(self):
        return f"{self.title} - {self.profile.user.get_full_name()}"

class IncidentFile(models.Model):
    incident = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='incident_files/%Y/%m/%d/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.incident.title} - {self.file.name}"

class IncidentNote(models.Model):
    incident = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.incident.title} by {self.created_by.get_full_name()}"