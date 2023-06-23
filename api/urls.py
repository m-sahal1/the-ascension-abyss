from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path("", getOverview, name="get-overview" ),
    # View all the elevator systems
    path("system/all", ElevatorSystemList.as_view(), name="system-list"),
    # Create new elevator systems
    path("system/add-new/", CreateElevatorSystem.as_view(), name="add-els"),
    # List all the elevators under an elevator system
    path("system/<int:id>/", ElevatorsList.as_view(), name="elevator-list"),
    # when dealing with single elevator
    # view
    path(
        "system/<int:id>/elevator/<int:pk>/view/",
        ViewSingleElevator.as_view(),
        name="elevator-view",
    ),
    # update
    path(
        "system/<int:id>/elevator/<int:pk>/update/",
        UpdateSingleElevator.as_view(),
        name="elevator-update",
    ),
    # Get destination
    path(
        "system/<int:id>/elevator/<int:pk>/destination/",
        GetDestination.as_view(),
        name="fetch-destination",
    ),
    #mark for maintenance
    path(
        "system/<int:sys>/elevator/<int:pk>/maintenance/",
        MaintenanceViewSet.as_view({'patch': 'mark_elevator_maintenance'}),
        name="maintenance",
    ),

    #open/close doors
    path(
        "system/<int:sys>/elevator/<int:pk>/doors/",
        ElevatorDoorViewSet.as_view({'patch': 'open_close_door'}),
        name="change-doors",
    ),

    # Request to an elevator
    # create
    path(
        "system/<int:id>/elevator/<int:pk>/req/add-new/",
        CreateElevatorRequest.as_view(),
        name="add-new-req",
    ),
    # view
    path(
        "system/<int:id>/elevator/<int:pk>/req/view/",
        ElevatorRequestList.as_view(),
        name="req-list",
    ),
]
