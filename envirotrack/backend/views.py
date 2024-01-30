from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import Serializer
from rest_framework import status

from .models import Responsible, Room, Profession, EnviromentalParameters, User
from .serializers import EnvironmentalParametersSerializer, RoomSelectSerializer, ResponsibleSerializer


def getRoutes(request):
    routes = [
        '/backend/token',
        '/backend/token/refresh'
    ]
    return Response(routes, safe=False)


@api_view(['GET'])
def getEnviromentalParameters(request):
    parameters = EnviromentalParameters.objects.all()
    serializer = EnvironmentalParametersSerializer(parameters, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def getEnviromentalParameter(request, pk):
    parameters = EnviromentalParameters.objects.get(id=pk)
    serializer = EnvironmentalParametersSerializer(parameters, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSelectSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createEnvironmentalParameters(request):
    serializer = EnvironmentalParametersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateEnvironmentalParameters(request, pk):
    try:
        environmental_params = EnviromentalParameters.objects.get(pk=pk)
    except EnviromentalParameters.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EnvironmentalParametersSerializer(instance=environmental_params, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteEnvironmentalParameters(request, pk):
    try:
        environmental_params = EnviromentalParameters.objects.get(pk=pk)
    except EnviromentalParameters.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    environmental_params.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    if user.is_authenticated:
        try:
            responsible = Responsible.objects.get(user=user)
            serializer = ResponsibleSerializer(responsible)
            return Response(serializer.data)
        except Responsible.DoesNotExist:
            return Response({'error': 'Responsible not found'}, status=404)
    else:
        return Response({'error': 'User not authenticated'}, status=401)