from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def getOverview(request):
    api_urls={
        'List': '/list',
        'Initialise_the_elevator_system': '/init',
        'List3': '/list3',
        'List4': '/list4',
        'List5': '/list5',
    }

    return Response(api_urls)