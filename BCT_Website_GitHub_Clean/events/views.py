from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Event, EventParticipant
from .forms import EventForm


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
    events = Event.objects.filter(
        date__gte=timezone.now()
    ).annotate(
        yes_count=Count('participants', filter=Q(participants__status='yes')),
        no_count=Count('participants', filter=Q(participants__status='no'))
    ).order_by('date')
    
    for event in events:
        try:
            participant = EventParticipant.objects.get(event=event, user=request.user)
            event.user_status = participant.status
        except EventParticipant.DoesNotExist:
            event.user_status = None
    
    context = {
        'events': events,
        'is_teamleader': is_teamleader(request.user),
    }
    return render(request, 'events/index.html', context)

@login_required
def detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    user_response = None
    try:
        participant = EventParticipant.objects.get(event=event, user=request.user)
        user_response = participant.status
    except EventParticipant.DoesNotExist:
        pass
    
    user_is_teamleader = is_teamleader(request.user)
    can_see_participants = event.participants_visible_to == 'everyone' or user_is_teamleader
    
    yes_responses = event.participants.filter(status='yes') if can_see_participants else None
    no_responses = event.participants.filter(status='no') if can_see_participants else None
    
    yes_count = event.participants.filter(status='yes').count()
    no_count = event.participants.filter(status='no').count()
    
    context = {
        'event': event,
        'user_response': user_response,
        'yes_responses': yes_responses,
        'no_responses': no_responses,
        'yes_count': yes_count,
        'no_count': no_count,
        'can_see_participants': can_see_participants,
        'is_teamleader': user_is_teamleader,
    }
    return render(request, 'events/detail.html', context)

@login_required
def rsvp(request, pk):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('events:detail', pk=pk)
    
    event = get_object_or_404(Event, pk=pk)
    status = request.POST.get('status')
    
    if status not in ['yes', 'no']:
        messages.error(request, "Invalid response. Please select Yes or No.")
        return redirect('events:detail', pk=pk)
    
    if status == 'yes' and event.is_full():
        existing = EventParticipant.objects.filter(event=event, user=request.user, status='yes').exists()
        if not existing:
            messages.error(request, "Sorry, this event is full.")
            return redirect('events:detail', pk=pk)
    
    participant, created = EventParticipant.objects.update_or_create(
        event=event,
        user=request.user,
        defaults={'status': status}
    )
    
    if status == 'yes':
        messages.success(request, "✓ Great! You've confirmed your attendance.")
    else:
        messages.success(request, "Your response has been recorded.")
    
    return redirect('events:detail', pk=pk)


@login_required
def create_event(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can create events.")
        return redirect('events:index')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Create New Event',
        'submit_text': 'Create Event',
    }
    return render(request, 'events/form.html', context)


@login_required
def edit_event(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can edit events.")
        return redirect('events:detail', pk=pk)
    
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'title': 'Edit Event',
        'submit_text': 'Save Changes',
    }
    return render(request, 'events/form.html', context)


@login_required
def delete_event(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can delete events.")
        return redirect('events:detail', pk=pk)
    
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f"Event '{event_title}' has been deleted.")
        return redirect('events:index')
    
    context = {
        'event': event,
    }
    return render(request, 'events/confirm_delete.html', context)
