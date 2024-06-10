from django.urls import path
from .views import FeedbackCreateView

urlpatterns = [
    path('api/feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
]
