from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from .serializers import (
    ElevatorSerializer,
    FloorRequestSerializer,
    InitializeElevatorSystemSerializer,
    FloorRequestSerializerAll
)
from .models import Elevator, FloorRequest, ElevatorSystem
from django_filters.rest_framework import DjangoFilterBackend

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


class ElevatorSystemList(generics.ListAPIView):
    """
    Fetch all the listed elevator systems.
    """

    queryset = ElevatorSystem.objects.all()
    serializer_class = InitializeElevatorSystemSerializer


class CreateElevatorSystem(generics.CreateAPIView):
    """
    Create a new elevator system.
    """

    serializer_class = InitializeElevatorSystemSerializer

    # Overriding the perform_create method of 'mixins.CreateModelMixin', Parent class of 'CreateAPIView'
    def perform_create(self, serializer):
        serializer.save()

        # Creating elevators needed for the system. For more details check create_elevators.py
        create_elevators(
            number_of_elevators=serializer.data["total_floors"],
            system_id=serializer.data["id"],
        )


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


class ElevatorDoorViewSet(viewsets.ViewSet):
    @action(detail=True, methods=["patch"])
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


class ElevatorsList(generics.ListAPIView):
    """
    Given an elevator system list all the elevators and their status.
    """

    serializer_class = ElevatorSerializer

    def get_queryset(self):
        system_id = self.kwargs["id"]
        queryset = Elevator.objects.filter(elevator_system__id=system_id)

        return queryset


class ViewSingleElevator(generics.RetrieveAPIView):
    """
    Get details of a specific elevator,
    given its elevator system and elevator number with URL
    """

    serializer_class = ElevatorSerializer

    def get_object(self):
        system_id = self.kwargs["id"]
        elevator_number = self.kwargs["pk"]

        queryset = Elevator.objects.filter(
            elevator_system__id=system_id, elevator_number=elevator_number
        )

        return queryset[0]


class UpdateSingleElevator(generics.UpdateAPIView):
    """
    Update details of a specific elevator,
    given its elevator system and elevator number with URL
    It can be done together with the previous view,
    but repeated for better understanding.
    """

    serializer_class = ElevatorSerializer

    def get_object(self):
        system_id = self.kwargs["id"]
        elevator_number = self.kwargs["pk"]

        queryset = Elevator.objects.filter(
            elevator_system__id=system_id, elevator_number=elevator_number
        )

        return queryset[0]

    # overriding put method by patch
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateElevatorRequest(generics.CreateAPIView):
    """
    Create a new request for a specific elevator,
    given its elevator system and elevator number with URL.
    The inputs of requested and destinatiom floor is sent with
    the form-data.
    """

    serializer_class = FloorRequestSerializer

    def perform_create(self, serializer):
        system_id = self.kwargs["id"]
        elevator_number = self.kwargs["pk"]

        queryset = Elevator.objects.filter(
            elevator_system__id=system_id, elevator_number=elevator_number
        )
        elevator_object = queryset[0]

        serializer.save(elevator=elevator_object)


class ElevatorRequestList(generics.ListAPIView):
    """
    List all the requests for a given elevator
    Requests already served can be filtered with is_active
    parameter set false

    """

    serializer_class = FloorRequestSerializerAll
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active"]

    def get_queryset(self):
        system_id = self.kwargs["id"]
        elevator_number = self.kwargs["pk"]

        elevator_object = Elevator.objects.filter(
            elevator_system__id=system_id, elevator_number=elevator_number
        )

        queryset = FloorRequest.objects.filter(elevator=elevator_object[0])
        return queryset


class GetDestination(APIView):
    '''
    Fetch the next destination floor for a given elevator
    '''
    def get(self, request,id,pk):
        system_id = id
        elevator_number = pk

        elevator_object = Elevator.objects.filter(
        elevator_system__id = system_id,
        elevator_number = elevator_number
        )

        requests_pending = FloorRequest.objects.filter(
        elevator = elevator_object[0],
        is_active = True,
        ).order_by('request_time')
        return Response(FloorRequestSerializer(requests_pending))


# functions
def create_elevators(total_elevators: int, sysId: int):
    """
    Function to automatically create elevators inside an elevator system
    Given the system id and number of elevators. This function is ran once
    an elevator system is created
    """

    for i in range(1,total_elevators):
        elevator_object = Elevator.objects.create(
            elevator_system_id=sysId,
            elevator_number=i + 1,
        )

        elevator_object.save()
