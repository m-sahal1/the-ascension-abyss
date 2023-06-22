from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (
    ElevatorSerializer,
    FloorRequestSerializer,
    InitializeElevatorSystemSerializer,
)
from .models import Elevator, FloorRequest


# Create your views here.
@api_view(["GET"])
def getOverview(request):
    api_urls = {
        "View all elevators": "/all",
        "Initialise_the_elevator_system": "/init",
        "Fetch all requests for the given elevator": "/requests/<elevator-id>",
        "Fetch the next destination floor for an elevator": "next-destination/<elevator-id>",
        "Fetch the direction of elevator": "status/<elevator-id>",
        "Save user request for the elevator": "add-requests/<elevator-id>",
        "Open/Close the door of the elevator": "door/<elevator-id>",
        "Mark an elevator as not-working/in-maintenance": "maintenance/<elevator-id>",
    }

    return Response(api_urls)


@api_view(["GET"])
def getData(request):
    elevators = Elevator.objects.all()
    serializer = ElevatorSerializer(elevators, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def initialize_elevators(request):
    # clear the previous elevators and floors
    delete = Elevator.objects.all().delete()
    delete = FloorRequest.objects.all().delete()

    # add new elevators and floors to the system
    total_floors = request.data.get("total_floors")
    total_elevators = request.data.get("total_elevators")

    for i in range(total_elevators):
        elevator = Elevator()
        elevator.save()

    elevators = Elevator.objects.all()
    return Response({"message": "Elevators initialized successfully"})


@api_view(["GET"])
def get_elevator_requests(request, pk):
    # Logic to fetch all requests for the given elevator
    # ...

    return Response({"requests": requests})


@api_view(["GET"])
def get_next_destination(request, pk):
    # Logic to fetch the next destination floor for the given elevator
    # ...

    return Response({"destination_floor": destination_floor})


@api_view(["GET"])
def get_elevator_direction(request, pk):
    # Logic to fetch if the elevator is moving up or down currently
    # ...

    return Response({"direction": direction})


@api_view(["POST"])
def save_user_request(request, pk):
    # Logic to save user request to the list of requests for the elevator
    # ...

    return Response({"message": "User request saved successfully"})


@api_view(["PATCH"])
def mark_elevator_maintenance(request, pk):
    try:
        elevator = Elevator.objects.get(id=pk)
    except Elevator.DoesNotExist:
        return Response({"message": "Elevator not found"}, status=404)

    # Update the maintenance status
    elevator.operational = request.data.get(
        "operational"
    )  # Set the maintenance field to True or False based on your requirement
    elevator.save()

    serializer = ElevatorSerializer(elevator)

    return Response(serializer.data)


@api_view(["PATCH"])
def open_close_door(request, pk):
    try:
        elevator = Elevator.objects.get(id=pk)
    except Elevator.DoesNotExist:
        return Response({"message": "Elevator not found"}, status=404)
#if the elevator is moving we cannot open the doors
    if(elevator.status=='moving_up' or elevator.status=='moving_down'):
        return Response({"message": "Can't open doors when elevator is moving"})
    # Update the maintenance status
    else:
        elevator.door = request.data.get(
            "door"
        )  # Set the maintenance field to True or False based on your requirement
        elevator.save()

        serializer = ElevatorSerializer(elevator)

        return Response({"message": f"Door status changed to {elevator.door}"})
