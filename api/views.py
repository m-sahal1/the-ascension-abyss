from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from .serializers import (
    ElevatorSerializer,
    FloorRequestSerializer,
    InitializeElevatorSystemSerializer,
)
from .models import Elevator, FloorRequest, ElevatorSystem


# API endpoint to get an overview of available API URLs
@api_view(["GET"])
def getOverview(request):
    """
    Returns a dictionary containing the available API URLs.
    """
    api_urls = {
        "View all elevators": "/all",
        "Initialise_the_elevator_system": "/init",
        "Fetch all requests for the given elevator": "/requests/<elevator-id>",
        "Fetch the next destination floor for an elevator": "next-destination/<elevator-id>",
        "Fetch the direction of elevator": "status/<elevator-id>",
        "Save user request for the elevator": "add-requests/",
        "Open/Close the door of the elevator": "door/<elevator-id>",
        "Mark an elevator as not-working/in-maintenance": "maintenance/<elevator-id>",
    }
    return Response(api_urls)


# API endpoint to get data of all elevators
@api_view(["GET"])
def getData(request):
    """
    Returns the data of all elevators.
    """
    elevators = Elevator.objects.all()
    serializer = ElevatorSerializer(elevators, many=True)
    return Response(serializer.data)


class ElevatorSystemList(generics.ListAPIView):
    """
    Fetch all the listed elevator systems.
    """

    elevatorSystems = ElevatorSystem.objects.all()
    serializer_class = InitializeElevatorSystemSerializer


class CreateElevatorSystem(generics.CreateAPIView):
    """
    Create a new elevator system.
    """

    serializer_class = InitializeElevatorSystemSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create_elevators(self):
        number_of_elevators = self.request.data.get("total_elevators")
        system_id = self.request.data.get("id")

        if number_of_elevators is None or system_id is None:
            # Handle missing input data appropriately
            return

        for i in range(int(number_of_elevators)):
            elevator = Elevator.objects.create(
                elevator_system_id=system_id,
                elevator_number=i + 1,
            )
            elevator.save()




# API endpoint to get all requests for a given elevator
@api_view(["GET"])
def get_elevator_requests(request, pk):
    """
    Returns all requests for the given elevator.
    """

    elevator = Elevator.objects.get(id=pk)

    return Response({"requests": requests})


# API endpoint to get the next destination floor for an elevator
@api_view(["GET"])
def get_next_destination(request, pk):
    """
    Returns the next destination floor for the given elevator and updates its status and current floor.
    """
    try:
        elevator = Elevator.objects.get(id=pk)
    except Elevator.DoesNotExist:
        return Response({"message": "Elevator not found"}, status=404)

    destination_floor = request.data.get("destination_floor")
    current_floor = request.data.get("current_floor")

    if destination_floor - current_floor == 0:
        elevator.status = "idle"
    elif destination_floor - current_floor > 0:
        elevator.status = "moving_up"
    else:
        elevator.status = "moving_down"

    # Assumption: Assume the API calls which make the elevator go up/down or stop will reflect
    # immediately. When the API to go up is called, you can assume that the elevator has already
    # reached the above floor.
    elevator.destination_floor = destination_floor
    elevator.current_floor = destination_floor
    return Response({"destination_floor": destination_floor})


# API endpoint to get the direction of an elevator
@api_view(["GET"])
def get_elevator_direction(request, pk):
    """
    Returns the direction (moving up/moving down) of the given elevator.
    """
    try:
        elevator = Elevator.objects.get(id=pk)
    except Elevator.DoesNotExist:
        return Response({"message": "Elevator not found"}, status=404)
    direction = elevator.status
    return Response({"direction": direction})


# API endpoint to save a user request for an elevator
@api_view(["POST"])
def save_user_request(request):
    """
    Saves a user request for an elevator.
    """
    serializer = FloorRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    serializer = FloorRequestSerializer(FloorRequest.objects.all(), many=True)
    return Response(serializer.data)


class MaintenanceViewSet(viewsets.ViewSet):
    @action(detail=True, methods=["patch"])
    def mark_elevator_maintenance(self, request, pk=None):
        try:
            elevator = Elevator.objects.get(id=pk)
        except Elevator.DoesNotExist:
            return Response({"message": "Elevator not found"}, status=404)

        # Update the maintenance status
        elevator.operational = request.data.get("operational")
        elevator.save()

        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)


# # API endpoint to mark an elevator as not working or in maintenance
# @api_view(["PATCH"])
# def mark_elevator_maintenance(request, pk):
#     """
#     Marks the given elevator as not working or in maintenance.
#     """
#     try:
#         elevator = Elevator.objects.get(id=pk)
#     except Elevator.DoesNotExist:
#         return Response({"message": "Elevator not found"}, status=404)
#     # Update the maintenance status
#     elevator.operational = request.data.get(
#         "operational"
#     )  # Set the maintenance field to True or False based on your requirement
#     elevator.save()
#     serializer = ElevatorSerializer(elevator)
#     return Response(serializer.data)

class ElevatorDoorViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['patch'])
    def open_close_door(self, request, pk=None):
        try:
            elevator = Elevator.objects.get(id=pk)
        except Elevator.DoesNotExist:
            return Response({"message": "Elevator not found"}, status=404)

        # If the elevator is moving, we cannot open the doors
        if elevator.status == "moving_up" or elevator.status == "moving_down":
            return Response({"message": "Can't open doors when elevator is moving"})
        # Update the door status
        else:
            elevator.door = request.data.get("door")
            elevator.save()
            serializer = ElevatorSerializer(elevator)
            return Response({"message": f"Door status changed to {elevator.door}"})
# # API endpoint to open or close the door of an elevator
# @api_view(["PATCH"])
# def open_close_door(request, pk):
#     """
#     Opens or closes the door of the given elevator based on the request data.
#     """
#     try:
#         elevator = Elevator.objects.get(id=pk)
#     except Elevator.DoesNotExist:
#         return Response({"message": "Elevator not found"}, status=404)

#     # If the elevator is moving, we cannot open the doors
#     if elevator.status == "moving_up" or elevator.status == "moving_down":
#         return Response({"message": "Can't open doors when elevator is moving"})
#     # Update the door status
#     else:
#         elevator.door = request.data.get(
#             "door"
#         )  # Set the door field to "open" or "close" based on your requirement
#         elevator.save()

#         serializer = ElevatorSerializer(elevator)

#         return Response({"message": f"Door status changed to {elevator.door}"})
