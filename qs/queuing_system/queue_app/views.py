from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Queue
from .forms import RegisterForm, TableNumberForm
import time
import json

# Global lists to store the last four served ticket numbers for each queue type
last_served_bachelor = []
last_served_magistracy = []

# Global variable to store the last served ticket number for announcement
last_served_ticket = None

def index(request):
    new_ticket_number = request.GET.get('new_ticket_number', None)
    return render(request, 'queue_app/index.html', {'new_ticket_number': new_ticket_number})

def new_ticket(request, queue_type):
    if request.method == 'POST':
        ticket_number = Queue.generate_next_ticket_number(queue_type)
        Queue.objects.create(ticket_number=ticket_number, queue_type=queue_type)
        return redirect(f'/?new_ticket_number={ticket_number}')
    return redirect('index')

@login_required
def operator_view(request):
    table_form = TableNumberForm()
    return render(request, 'queue_app/operator.html', {'table_form': table_form})

@login_required
def serve_ticket(request, ticket_id):
    global last_served_bachelor, last_served_magistracy, last_served_ticket
    if request.method == 'POST':
        form = TableNumberForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data['table_number']
            ticket = Queue.objects.get(id=ticket_id)
            ticket.served = True
            ticket.served_by_table = table_number
            ticket.save()
            last_served_ticket = ticket.ticket_number
            if ticket.queue_type == 'B':
                last_served_bachelor.append({'ticket_number': ticket.ticket_number, 'served_by_table': table_number})
                if len(last_served_bachelor) > 4:
                    last_served_bachelor.pop(0)  # Keep only the last 4 tickets
            else:
                last_served_magistracy.append({'ticket_number': ticket.ticket_number, 'served_by_table': table_number})
                if len(last_served_magistracy) > 4:
                    last_served_magistracy.pop(0)  # Keep only the last 4 tickets
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
    return redirect('operator')

@login_required
def sse_operator(request):
    def event_stream():
        while True:
            bachelor_queue = Queue.objects.filter(queue_type='B', served=False).order_by('created_at')
            magistracy_queue = Queue.objects.filter(queue_type='M', served=False).order_by('created_at')
            queue_data = {
                'bachelor': [{'id': ticket.id, 'ticket_number': ticket.ticket_number} for ticket in bachelor_queue],
                'magistracy': [{'id': ticket.id, 'ticket_number': ticket.ticket_number} for ticket in magistracy_queue],
            }
            yield f'data: {json.dumps(queue_data)}\n\n'
            time.sleep(1)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

def monitor_view(request):
    bachelor_queue = Queue.objects.filter(queue_type='B', served=False).order_by('created_at')
    magistracy_queue = Queue.objects.filter(queue_type='M', served=False).order_by('created_at')
    return render(request, 'queue_app/monitor.html', {'bachelor_queue': bachelor_queue, 'magistracy_queue': magistracy_queue})

def sse(request):
    def event_stream():
        global last_served_bachelor, last_served_magistracy, last_served_ticket
        while True:
            bachelor_queue = Queue.objects.filter(queue_type='B', served=False).order_by('created_at')
            magistracy_queue = Queue.objects.filter(queue_type='M', served=False).order_by('created_at')
            queue_data = {
                'bachelor': [{'id': ticket.id, 'ticket_number': ticket.ticket_number} for ticket in bachelor_queue],
                'magistracy': [{'id': ticket.id, 'ticket_number': ticket.ticket_number} for ticket in magistracy_queue],
                'last_served_bachelor': last_served_bachelor,
                'last_served_magistracy': last_served_magistracy,
                'last_served_ticket': last_served_ticket
            }
            yield f'data: {json.dumps(queue_data)}\n\n'
            last_served_ticket = None  # Reset after sending
            time.sleep(1)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('operator')
    else:
        form = RegisterForm()
    return render(request, 'queue_app/register.html', {'form': form})
