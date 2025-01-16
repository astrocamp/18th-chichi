from django.urls import path
from . import views

urlpatterns = [
    path(
        "calendar-events/",
        views.project_calendar_events,
        name="calendar_events",
    ),
    path(
        "calendar-events/add/",
        views.add_calendar_event,
        name="add_calendar_event",
    ),
    path(
        "calendar-events/<int:event_id>/update/",
        views.update_calendar_event,
        name="update_calendar_event",
    ),
    path(
        "calendar-events/<int:event_id>/delete/",
        views.delete_calendar_event,
        name="delete_calendar_event",
    ),
]
