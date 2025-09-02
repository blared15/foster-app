from django.contrib import admin
from .models import IncidentReport, IncidentFile, IncidentNote

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'incident_type', 'severity', 'status', 'reported_by', 'incident_date')
    list_filter = ('severity', 'status', 'incident_type', 'incident_date')
    search_fields = ('title', 'description', 'profile__user__username', 'profile__user__first_name', 'profile__user__last_name')
    readonly_fields = ('reported_by', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(IncidentFile)
class IncidentFileAdmin(admin.ModelAdmin):
    list_display = ('incident', 'file', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_by', 'uploaded_at')

@admin.register(IncidentNote)
class IncidentNoteAdmin(admin.ModelAdmin):
    list_display = ('incident', 'created_by', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_by', 'created_at', 'updated_at')