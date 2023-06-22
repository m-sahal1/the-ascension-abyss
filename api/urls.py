from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.getOverview, name='get-overview'),
    path('all/', views.getData, name='get-data'),
    path('init/', views.initialize_elevators, name='initialize-elevators'),
    path('requests/<str:pk>', views.get_elevator_requests, name='elevator-requests'),
    path('next-destination/<str:pk>', views.get_next_destination, name='next-destination'),
    path('status/<str:pk>', views.get_elevator_direction, name='elevator-status'),
    path('add-requests/<str:pk>', views.save_user_request, name='add-requests'),
    path('maintenance/<str:pk>', views.mark_elevator_maintenance, name='mark-maintenance'),
    path('door/<str:pk>', views.open_close_door, name='door'),
]
