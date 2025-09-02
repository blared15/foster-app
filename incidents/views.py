from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import IncidentReport, IncidentFile, IncidentNote
from .forms import IncidentReportForm, IncidentFileForm, IncidentNoteForm
from accounts.models import Profile

@login_required
def incident_list(request):
    # Filter incidents based on user role
    if request.user.profile.role == 'admin':
        incidents = IncidentReport.objects.all()
    else:
        # Staff can see incidents they reported or are assigned to
        incidents = IncidentReport.objects.filter(
            Q(reported_by=request.user) | Q(assigned_to=request.user)
        )
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        incidents = incidents.filter(status=status_filter)
    
    # Filter by severity if provided
    severity_filter = request.GET.get('severity')
    if severity_filter:
        incidents = incidents.filter(severity=severity_filter)
    
    context = {
        'incidents': incidents,
        'status_filter': status_filter,
        'severity_filter': severity_filter,
    }
    return render(request, 'incidents/incident_list.html', context)

@login_required
def incident_detail(request, incident_id):
    incident = get_object_or_404(IncidentReport, id=incident_id)
    
    # Check if user has permission to view this incident
    if (request.user.profile.role != 'admin' and 
        incident.reported_by != request.user and 
        incident.assigned_to != request.user):
        messages.error(request, 'You do not have permission to view this incident.')
        return redirect('incident_list')
    
    file_form = IncidentFileForm()
    note_form = IncidentNoteForm()
    
    if request.method == 'POST':
        if 'add_file' in request.POST:
            file_form = IncidentFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                incident_file = file_form.save(commit=False)
                incident_file.incident = incident
                incident_file.uploaded_by = request.user
                incident_file.save()
                messages.success(request, 'File uploaded successfully!')
                return redirect('incident_detail', incident_id=incident.id)
        
        elif 'add_note' in request.POST:
            note_form = IncidentNoteForm(request.POST)
            if note_form.is_valid():
                incident_note = note_form.save(commit=False)
                incident_note.incident = incident
                incident_note.created_by = request.user
                incident_note.save()
                messages.success(request, 'Note added successfully!')
                return redirect('incident_detail', incident_id=incident.id)
    
    context = {
        'incident': incident,
        'file_form': file_form,
        'note_form': note_form,
    }
    return render(request, 'incidents/incident_detail.html', context)

@login_required
def incident_create(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()
            messages.success(request, 'Incident report created successfully!')
            return redirect('incident_detail', incident_id=incident.id)
    else:
        form = IncidentReportForm()
    
    context = {'form': form}
    return render(request, 'incidents/incident_form.html', context)

@login_required
def incident_edit(request, incident_id):
    incident = get_object_or_404(IncidentReport, id=incident_id)
    
    # Check if user has permission to edit this incident
    if (request.user.profile.role != 'admin' and 
        incident.reported_by != request.user):
        messages.error(request, 'You do not have permission to edit this incident.')
        return redirect('incident_list')
    
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            messages.success(request, 'Incident report updated successfully!')
            return redirect('incident_detail', incident_id=incident.id)
    else:
        form = IncidentReportForm(instance=incident)
    
    context = {'form': form, 'incident': incident}
    return render(request, 'incidents/incident_form.html', context)

@login_required
def incident_update_status(request, incident_id):
    incident = get_object_or_404(IncidentReport, id=incident_id)
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        new_status = request.POST.get('status')
        if new_status in dict(IncidentReport.STATUS_CHOICES):
            incident.status = new_status
            incident.save()
            return JsonResponse({'success': True, 'new_status': incident.get_status_display()})
    
    return JsonResponse({'success': False})

@login_required
def incident_dashboard(request):
    # Get statistics for dashboard
    total_incidents = IncidentReport.objects.count()
    open_incidents = IncidentReport.objects.filter(status='open').count()
    high_severity = IncidentReport.objects.filter(severity='high').count()
    critical_severity = IncidentReport.objects.filter(severity='critical').count()
    
    # Recent incidents
    recent_incidents = IncidentReport.objects.all().order_by('-incident_date')[:5]
    
    # Incidents by type
    incidents_by_type = {}
    for incident_type in IncidentReport.INCIDENT_TYPES:
        count = IncidentReport.objects.filter(incident_type=incident_type[0]).count()
        incidents_by_type[incident_type[1]] = count
    
    context = {
        'total_incidents': total_incidents,
        'open_incidents': open_incidents,
        'high_severity': high_severity,
        'critical_severity': critical_severity,
        'recent_incidents': recent_incidents,
        'incidents_by_type': incidents_by_type,
    }
    return render(request, 'incidents/incident_dashboard.html', context)