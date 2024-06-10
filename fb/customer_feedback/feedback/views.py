from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from rest_framework import generics
from .models import Feedback
from .serializers import FeedbackSerializer

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_thanks')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})

def feedback_thanks(request):
    return render(request, 'feedback/thanks.html')

class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
