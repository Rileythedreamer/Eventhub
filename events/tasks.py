from celery import shared_task
from django.utils import timezone
from .models import Event

@shared_task
def update_past_events_status():
    past_events = []
    events = Event.objects.all()
    for event in events:
        if event.is_passed():
            event.is_passed()
            past_events.append(event)
    return f"Updated {past_events} events to past status."
