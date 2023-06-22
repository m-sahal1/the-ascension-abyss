from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    # View all the elevator systems
    path("sys/all", ElevatorSystemList.as_view(), name="el-sys-list"),
    # Create new elevator systems
    path("sys/add-new/", CreateElevatorSystem.as_view(), name="add-new-els"),
    # List all the elevators under an elevator system
    path("elevator/<int:id>/", ElevatorsList.as_view(), name="elevator-list"),
    # single elevator
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
    # Fetch destination
    path(
        "system/<int:id>/elevator/<int:pk>/destination/",
        FetchDestination.as_view(),
        name="fetch-destination",
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
