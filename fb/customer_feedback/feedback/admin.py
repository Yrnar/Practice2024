from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer_name', 'comment')

admin.site.register(Feedback, FeedbackAdmin)
