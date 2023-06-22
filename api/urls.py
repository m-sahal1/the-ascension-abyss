from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.getOverview, name='get-overview'),
    path('initialize/', views.initialize_elevators, name='initialize-elevators'),
    path('', views.getOverview, name='get-overview'),
    path('', views.getOverview, name='get-overview'),
]
