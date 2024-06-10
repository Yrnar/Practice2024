from django.contrib import admin
from .models import Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'queue_type', 'created_at', 'served')
    list_filter = ('queue_type', 'served')
    search_fields = ('ticket_number',)
    ordering = ('-created_at',)
