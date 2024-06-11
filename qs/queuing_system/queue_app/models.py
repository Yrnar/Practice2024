from django.db import models
from django.utils import timezone

class Queue(models.Model):
    QUEUE_TYPE_CHOICES = [
        ('B', 'Bachelor'),
        ('M', 'Magistracy'),
    ]
    ticket_number = models.CharField(max_length=10, default='0000')
    queue_type = models.CharField(max_length=1, choices=QUEUE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    served = models.BooleanField(default=False)

    @staticmethod
    def generate_next_ticket_number(queue_type):
        last_ticket = Queue.objects.filter(queue_type=queue_type).order_by('created_at').last()
        if not last_ticket:
            return f"{queue_type}001"
        last_ticket_number = int(last_ticket.ticket_number[1:])
        new_ticket_number = last_ticket_number + 1
        return f"{queue_type}{str(new_ticket_number).zfill(3)}"

    @staticmethod
    def reset_ticket_numbers():
        queues = Queue.objects.all()
        for queue in queues:
            queue.ticket_number = '0000'
            queue.save()

    def __str__(self):
        return f"{self.get_queue_type_display()} - {self.ticket_number}"
