from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import (
    SafetyInfo,
    WorkSafetyCategory,
    WorkSafetyDocument,
    WorkSafetyAcknowledgement,
    WorkSafetyEmergencyInfo,
    WorkSafetyIncidentReport
)
from .forms import (
    WorkSafetyDocumentForm,
    WorkSafetyCategoryForm,
    WorkSafetyEmergencyInfoForm,
    WorkSafetyIncidentReportForm,
    IncidentStatusForm
)


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.is_staff or
            user.groups.filter(name__iexact='teamleader').exists()
        )
    )


@login_required
def index(request):
    emergency_info = WorkSafetyEmergencyInfo.get_instance()
    categories = WorkSafetyCategory.objects.all()
    user_is_teamleader = is_teamleader(request.user)
    
    if user_is_teamleader:
        documents = WorkSafetyDocument.objects.select_related('category', 'created_by').all()
    else:
        documents = WorkSafetyDocument.objects.select_related('category', 'created_by').filter(
            status='active',
            visible_to='everyone'
        )
    
    for doc in documents:
        user_ack = doc.get_user_acknowledgement(request.user)
        doc.user_has_acknowledged = user_ack and user_ack.version == doc.version
        doc.needs_acknowledgement = doc.requires_acknowledgement_for(request.user)
        doc.user_ack_version = user_ack.version if user_ack else None
    
    docs_by_category = {}
    for cat in categories:
        cat_docs = [d for d in documents if d.category_id == cat.id]
        if cat_docs or user_is_teamleader:
            docs_by_category[cat] = cat_docs
    
    context = {
        'emergency_info': emergency_info,
        'categories': categories,
        'docs_by_category': docs_by_category,
        'documents': documents,
        'is_teamleader': user_is_teamleader,
    }
    return render(request, 'worksafety/index.html', context)


@login_required
def document_detail(request, pk):
    document = get_object_or_404(WorkSafetyDocument, pk=pk)
    user_is_teamleader = is_teamleader(request.user)
    
    if not user_is_teamleader:
        if document.status != 'active':
            messages.error(request, "This document is not available.")
            return redirect('worksafety:index')
        if document.visible_to == 'teamleaders':
            messages.error(request, "You don't have permission to view this document.")
            return redirect('worksafety:index')
    
    user_ack = document.get_user_acknowledgement(request.user)
    needs_acknowledgement = document.requires_acknowledgement_for(request.user)
    ack_count = document.get_acknowledgement_count()
    
    acknowledgements = None
    if user_is_teamleader:
        acknowledgements = document.acks.filter(version=document.version).select_related('user').order_by('-acknowledged_at')
    
    context = {
        'document': document,
        'user_ack': user_ack,
        'needs_acknowledgement': needs_acknowledgement,
        'ack_count': ack_count,
        'acknowledgements': acknowledgements,
        'is_teamleader': user_is_teamleader,
    }
    return render(request, 'worksafety/document_detail.html', context)


@login_required
def acknowledge_document(request, pk):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('worksafety:document_detail', pk=pk)
    
    document = get_object_or_404(WorkSafetyDocument, pk=pk)
    user_is_teamleader = is_teamleader(request.user)
    
    if not user_is_teamleader:
        if document.status != 'active':
            messages.error(request, "This document is not available for acknowledgement.")
            return redirect('worksafety:index')
        if document.visible_to == 'teamleaders':
            messages.error(request, "You don't have permission to acknowledge this document.")
            return redirect('worksafety:index')
    
    ack, created = WorkSafetyAcknowledgement.objects.get_or_create(
        document=document,
        user=request.user,
        version=document.version
    )
    
    if created:
        messages.success(request, f"✓ You have acknowledged '{document.title}' (version {document.version}).")
    else:
        messages.info(request, "You have already acknowledged this version of the document.")
    
    return redirect('worksafety:document_detail', pk=pk)


@login_required
def create_document(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can create safety documents.")
        return redirect('worksafety:index')
    
    if request.method == 'POST':
        form = WorkSafetyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = request.user
            document.save()
            messages.success(request, f"Document '{document.title}' created successfully!")
            return redirect('worksafety:document_detail', pk=document.pk)
    else:
        form = WorkSafetyDocumentForm()
    
    context = {
        'form': form,
        'title': 'Upload New Safety Document',
        'submit_text': 'Create Document',
    }
    return render(request, 'worksafety/document_form.html', context)


@login_required
def edit_document(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can edit safety documents.")
        return redirect('worksafety:document_detail', pk=pk)
    
    document = get_object_or_404(WorkSafetyDocument, pk=pk)
    
    if request.method == 'POST':
        old_version = document.version
        form = WorkSafetyDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            if old_version != document.version:
                messages.success(request, f"Document updated to version {document.version}. Users will need to re-acknowledge.")
            else:
                messages.success(request, f"Document '{document.title}' updated successfully!")
            return redirect('worksafety:document_detail', pk=document.pk)
    else:
        form = WorkSafetyDocumentForm(instance=document)
    
    context = {
        'form': form,
        'document': document,
        'title': 'Edit Safety Document',
        'submit_text': 'Save Changes',
    }
    return render(request, 'worksafety/document_form.html', context)


@login_required
def delete_document(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can delete safety documents.")
        return redirect('worksafety:document_detail', pk=pk)
    
    document = get_object_or_404(WorkSafetyDocument, pk=pk)
    
    if request.method == 'POST':
        document_title = document.title
        document.delete()
        messages.success(request, f"Document '{document_title}' has been deleted.")
        return redirect('worksafety:index')
    
    context = {
        'document': document,
    }
    return render(request, 'worksafety/confirm_delete.html', context)


@login_required
def manage_categories(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can manage categories.")
        return redirect('worksafety:index')
    
    categories = WorkSafetyCategory.objects.annotate(
        doc_count=Count('documents')
    ).order_by('order', 'name')
    
    context = {
        'categories': categories,
        'is_teamleader': True,
    }
    return render(request, 'worksafety/categories.html', context)


@login_required
def create_category(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can create categories.")
        return redirect('worksafety:index')
    
    if request.method == 'POST':
        form = WorkSafetyCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully!")
            return redirect('worksafety:manage_categories')
    else:
        form = WorkSafetyCategoryForm()
    
    context = {
        'form': form,
        'title': 'Create New Category',
        'submit_text': 'Create Category',
    }
    return render(request, 'worksafety/category_form.html', context)


@login_required
def edit_category(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can edit categories.")
        return redirect('worksafety:index')
    
    category = get_object_or_404(WorkSafetyCategory, pk=pk)
    
    if request.method == 'POST':
        form = WorkSafetyCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' updated successfully!")
            return redirect('worksafety:manage_categories')
    else:
        form = WorkSafetyCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': 'Edit Category',
        'submit_text': 'Save Changes',
    }
    return render(request, 'worksafety/category_form.html', context)


@login_required
def delete_category(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can delete categories.")
        return redirect('worksafety:index')
    
    category = get_object_or_404(WorkSafetyCategory, pk=pk)
    doc_count = category.documents.count()
    
    if doc_count > 0:
        messages.error(request, f"Cannot delete category '{category.name}' because it has {doc_count} document(s). Please reassign or delete the documents first.")
        return redirect('worksafety:manage_categories')
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' has been deleted.")
        return redirect('worksafety:manage_categories')
    
    context = {
        'category': category,
    }
    return render(request, 'worksafety/confirm_delete_category.html', context)


@login_required
def edit_emergency_info(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can edit emergency information.")
        return redirect('worksafety:index')
    
    emergency_info = WorkSafetyEmergencyInfo.get_instance()
    
    if request.method == 'POST':
        form = WorkSafetyEmergencyInfoForm(request.POST, instance=emergency_info)
        if form.is_valid():
            info = form.save(commit=False)
            info.updated_by = request.user
            info.save()
            messages.success(request, "Emergency information updated successfully!")
            return redirect('worksafety:index')
    else:
        form = WorkSafetyEmergencyInfoForm(instance=emergency_info)
    
    context = {
        'form': form,
        'title': 'Edit Emergency Information',
        'submit_text': 'Save Changes',
    }
    return render(request, 'worksafety/emergency_form.html', context)


@login_required
def report_incident(request):
    if request.method == 'POST':
        form = WorkSafetyIncidentReportForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.submitted_by = request.user
            incident.save()
            messages.success(request, "Incident report submitted successfully. Team leaders have been notified.")
            return redirect('worksafety:index')
    else:
        form = WorkSafetyIncidentReportForm(initial={'occurred_at': timezone.now()})
    
    context = {
        'form': form,
        'title': 'Report an Incident',
        'submit_text': 'Submit Report',
    }
    return render(request, 'worksafety/incident_form.html', context)


@login_required
def list_incidents(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can view incident reports.")
        return redirect('worksafety:index')
    
    incidents = WorkSafetyIncidentReport.objects.select_related('submitted_by').order_by('-occurred_at')
    
    context = {
        'incidents': incidents,
        'is_teamleader': True,
    }
    return render(request, 'worksafety/incidents_list.html', context)


@login_required
def incident_detail(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can view incident details.")
        return redirect('worksafety:index')
    
    incident = get_object_or_404(WorkSafetyIncidentReport, pk=pk)
    
    if request.method == 'POST':
        form = IncidentStatusForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            messages.success(request, f"Incident status updated to '{incident.get_status_display()}'.")
            return redirect('worksafety:incident_detail', pk=pk)
    else:
        form = IncidentStatusForm(instance=incident)
    
    context = {
        'incident': incident,
        'form': form,
        'is_teamleader': True,
    }
    return render(request, 'worksafety/incident_detail.html', context)
