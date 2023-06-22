from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ElevatorSerializer, FloorRequestSerializer, InitializeElevatorSystemSerializer
from .models import Elevator, FloorRequest
# Create your views here.
@api_view(['GET'])
def getOverview(request):
    api_urls={
        'List': '/list',
        'Initialise_the_elevator_system': '/initialize',
        'List3': '/list3',
        'List4': '/list4',
        'List5': '/list5',
    }

    return Response(api_urls)


@api_view(['POST'])
def initialize_elevators(request):
    #clear the previous elevators and floors
    delete=Elevator.objects.all().delete()
    delete=FloorRequest.objects.all().delete()


    #add new elevators and floors to the system
    total_floors = request.data.get('total_floors')
    total_elevators = request.data.get('total_elevators')
    # serializer=InitializeElevatorSystemSerializer(data=request.data)
    # if(serializer.is_valid()):
    #     serializer.save()

    for i in range(total_elevators):
        elevator= Elevator()
        elevator.save()

    elevators=Elevator.objects.all()
    return Response({'message': 'Elevators initialized successfully'})

# @api_view(['GET'])
# def get_elevator_requests(request, elevator_id):
#     # Logic to fetch all requests for the given elevator
#     # ...
    
#     return Response({'requests': requests})


# @api_view(['GET'])
# def get_next_destination(request, elevator_id):
#     # Logic to fetch the next destination floor for the given elevator
#     # ...
    
#     return Response({'destination_floor': destination_floor})

# @api_view(['GET'])
# def get_elevator_direction(request, elevator_id):
#     # Logic to fetch if the elevator is moving up or down currently
#     # ...
    
#     return Response({'direction': direction})

# @api_view(['POST'])
# def save_user_request(request, elevator_id):
#     # Logic to save user request to the list of requests for the elevator
#     # ...
    
#     return Response({'message': 'User request saved successfully'})

# @api_view(['POST'])
# def mark_elevator_maintenance(request, elevator_id):
#     # Logic to mark an elevator as not working or in maintenance
#     # ...
    
#     return Response({'message': 'Elevator marked as maintenance'})

# @api_view(['POST'])
# def open_close_door(request, elevator_id):
#     # Logic to open/close the door of the elevator
#     # ...
    
#     return Response({'message': 'Door status changed successfully'})