from django.contrib import admin
from .models import Queue

class QueueAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'queue_type', 'created_at', 'served', 'served_by_table')
    list_filter = ('queue_type', 'served', 'served_by_table')
    ordering = ('-created_at',)

admin.site.register(Queue, QueueAdmin)
