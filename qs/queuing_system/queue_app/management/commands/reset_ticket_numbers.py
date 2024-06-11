
from django.core.management.base import BaseCommand
from queue_app.models import Queue

class Command(BaseCommand):
    help = 'Reset all ticket numbers to 0000'

    def handle(self, *args, **kwargs):
        Queue.reset_ticket_numbers()
        self.stdout.write(self.style.SUCCESS('Successfully reset all ticket numbers to 0000'))
