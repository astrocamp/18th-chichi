import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

document.addEventListener('DOMContentLoaded', function () {
    initializeCalendar();
});

function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    const calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay',
        },
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        locale: 'zh-tw',
        height: 'auto',

        events: {
            url: '/projects/api/calendar-events/',
            method: 'GET',
        },

        select: function (info) {
            openEventDialog('create', null, info.start, info.end);
        },

        eventClick: function (info) {
            openEventDialog('edit', info.event);
        },

        eventDrop: function(info) {
            updateEvent(info.event);
        },

        eventResize: function(info) {
            updateEvent(info.event);
        }
    });

    calendar.render();
    setupEventHandlers(calendar);
}

function openEventDialog(mode, event, start = null, end = null) {
    const dialog = document.getElementById('eventDialog');
    const titleInput = document.getElementById('eventTitle');
    const startInput = document.getElementById('eventStart');
    const endInput = document.getElementById('eventEnd');
    const deleteButton = document.getElementById('deleteEvent');

    if (mode === 'edit' && event) {
        dialog.dataset.eventId = event.id;
        titleInput.value = event.title;
        startInput.value = formatDateTime(event.start);
        endInput.value = formatDateTime(event.end || event.start);
        deleteButton.style.display = 'block';
    } else {
        dialog.dataset.eventId = '';
        titleInput.value = '';
        startInput.value = formatDateTime(start);
        endInput.value = formatDateTime(end);
        deleteButton.style.display = 'none';
    }

    dialog.showModal();
}

async function updateEvent(event) {
    const eventData = {
        title: event.title,
        start_at: formatDateTime(event.start),
        end_at: formatDateTime(event.end || event.start),
    };

    try {
        const response = await fetch(`/projects/api/calendar-events/${event.id}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(eventData)
        });

        if (!response.ok) {
            event.revert();
            const errorData = await response.json();
            alert(`更新失敗: ${JSON.stringify(errorData)}`);
        }
    } catch (error) {
        event.revert();
        alert('更新失敗');
    }
}

function setupEventHandlers(calendar) {
    const saveButton = document.getElementById('saveEvent');
    const closeButton = document.getElementById('closeDialog');
    const deleteButton = document.getElementById('deleteEvent');
    const dialog = document.getElementById('eventDialog');

    if (saveButton) {
        saveButton.addEventListener('click', async () => {
            const eventId = dialog?.dataset.eventId;
            const title = document.getElementById('eventTitle')?.value.trim();
            const start_at = document.getElementById('eventStart')?.value;
            const end_at = document.getElementById('eventEnd')?.value;

            if (!title || !end_at) {
                alert('請填寫所有必填欄位');
                return;
            }

            const eventData = {
                title: title,
                start_at: start_at,
                end_at: end_at,
            };

            try {
                const url = eventId
                    ? `/projects/api/calendar-events/${eventId}/update/`
                    : '/projects/api/calendar-events/add/';
                const method = eventId ? 'PUT' : 'POST';

                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify(eventData),
                });

                if (response.ok) {
                    const eventData = await response.json();
                    if (eventId) {
                        const existingEvent = calendar.getEventById(eventId);
                        if (existingEvent) {
                            existingEvent.setProp('title', eventData.title);
                            existingEvent.setStart(eventData.start);
                            existingEvent.setEnd(eventData.end);
                        }
                    } else {
                        calendar.addEvent({
                            id: eventData.id,
                            title: eventData.title,
                            start: eventData.start,
                            end: eventData.end,
                        });
                    }
                    dialog?.close();
                } else {
                    const errorData = await response.json();
                    alert(`儲存失敗: ${JSON.stringify(errorData)}`);
                }
            } catch (error) {
                alert('儲存失敗');
            }
        });
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', async () => {
            const eventId = dialog?.dataset.eventId;
            if (!eventId) return;

            if (confirm('確定要刪除這個事件嗎？')) {
                try {
                    const response = await fetch(`/projects/api/calendar-events/${eventId}/delete/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    });

                    if (response.ok) {
                        const event = calendar.getEventById(eventId);
                        if (event) {
                            event.remove();
                        }
                        dialog?.close();
                    } else {
                        const errorData = await response.json();
                        alert(`刪除失敗: ${JSON.stringify(errorData)}`);
                    }
                } catch (error) {
                    alert('刪除失敗');
                }
            }
        });
    }

    if (closeButton) {
        closeButton.addEventListener('click', () => dialog?.close());
    }
}

function formatDateTime(date) {
    if (!date) return '';
    const d = new Date(date);
    if (isNaN(d.getTime())) return '';

    const pad = (num) => num.toString().padStart(2, '0');

    const year = d.getFullYear();
    const month = pad(d.getMonth() + 1);
    const day = pad(d.getDate());
    const hours = pad(d.getHours());
    const minutes = pad(d.getMinutes());

    return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}