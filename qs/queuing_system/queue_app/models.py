from django.db import models

class Queue(models.Model):
    TICKET_TYPES = [
        ('B', 'Bachelor'),
        ('M', 'Magistracy'),
    ]
    ticket_number = models.CharField(max_length=10)
    queue_type = models.CharField(max_length=1, choices=TICKET_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    served = models.BooleanField(default=False)

    @staticmethod
    def generate_next_ticket_number(queue_type):
        last_ticket = Queue.objects.filter(queue_type=queue_type).order_by('-created_at').first()
        if last_ticket:
            last_number = int(last_ticket.ticket_number[:-1])
            next_number = f"{last_number + 1:04d}"
        else:
            next_number = "0001"
        return f"{next_number}{queue_type}"
