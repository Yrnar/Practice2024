from django.contrib import admin
from django.urls import path
from queue_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new_ticket/<str:queue_type>/', views.new_ticket, name='new_ticket'),
    path('operator/', views.operator_view, name='operator'),
    path('monitor/', views.monitor_view, name='monitor'),
    path('serve_ticket/<int:ticket_id>/', views.serve_ticket, name='serve_ticket'),
    path('sse/', views.sse, name='sse'),
]
