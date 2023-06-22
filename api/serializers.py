from rest_framework import serializers
from .models import Elevator, FloorRequest

class InitializeElevatorSystemSerializer(serializers.Serializer):
    total_floors = serializers.IntegerField(min_value=1)
    total_elevators = serializers.IntegerField(min_value=1)
    

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Elevator
        fields='__all__'


class FloorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=FloorRequest
        fields='__all__'