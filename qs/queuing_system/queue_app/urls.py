from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_ticket/<str:queue_type>/', views.new_ticket, name='new_ticket'),
    path('operator/', views.operator_view, name='operator'),
    path('serve_ticket/<int:ticket_id>/', views.serve_ticket, name='serve_ticket'),
    path('sse_operator/', views.sse_operator, name='sse_operator'),
    path('monitor/', views.monitor_view, name='monitor'),
    path('sse/', views.sse, name='sse'),
    path('login/', auth_views.LoginView.as_view(template_name='queue_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='queue_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
