from rest_framework import serializers
from .models import Elevator, FloorRequest, ElevatorSystem


class InitializeElevatorSystemSerializer(serializers.ModelSerializer):
    """
    Model serializer for model ElevatorSystem
    """

    class Meta:
        model = ElevatorSystem
        fields = "__all__"

class ElevatorSerializer(serializers.ModelSerializer):
    """
    Model serializer for model Elevator
    """

    class Meta:
        model = Elevator
        fields = "__all__"


class FloorRequestSerializer(serializers.ModelSerializer):
    """
    Model serializer designed for ElevatorRequest
    it is utilized to handle POST requests with only two input arguments
    """

    class Meta:
        model = FloorRequest
        fields = (
            "requested_floor",
            "destination_floor",
        )

class FloorRequestSerializerAll(serializers.ModelSerializer):
    '''
    Model serializer for ElevatorRequest, used for 
    GET request that returns all the fields
    '''
    class Meta:
        model = FloorRequest
        fields = '__all__'