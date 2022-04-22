from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND
)

from basins import models
from . import serializers


@api_view(['POST'])
def basin_create(request):
    request_data = request.data
    request_data['belong_to'] = request.user.id
    serializer = serializers.BasinSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=HTTP_201_CREATED)
    return Response(status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def basins_list(request):
    basins = models.Basin.objects.filter(belong_to=request.user)
    serialized_basins = serializers.BasinSerializer(basins, many=True)
    return Response(serialized_basins.data, status=HTTP_200_OK)


@api_view(['GET'])
def basin_detail(request, pk):
    basin = models.Basin.objects.filter(pk=pk).first()
    if basin is not None:
        if basin.belong_to == request.user:
            serialized_basin = serializers.BasinSerializer(basin, many=False)
            return Response(serialized_basin.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_403_FORBIDDEN)
    else:
        return Response(status=HTTP_404_NOT_FOUND)


##############################################################


@api_view(['POST'])
@permission_classes([AllowAny])
def basin_message_create(request):
    serializer = serializers.BasinMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        basin_id = request.data.get('basin')
        basin = models.Basin.objects.filter(pk=basin_id).first()
        data = {
            'request': 'success',
            'height': basin.height,
            'phone': basin.phone
        }
        return Response(data, status=HTTP_201_CREATED)
    return Response(status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def basin_messages_list(request):
    messages = models.BasinMessage.objects.filter(basin__belong_to=request.user)
    serialized_messages = serializers.BasinMessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=HTTP_200_OK)


@api_view(['GET'])
def basin_message_detail(request, pk):
    message = models.BasinMessage.objects.filter(pk=pk).first()
    if message is not None:
        if message.basin.belong_to == request.user:
            serialized_message = serializers.BasinMessageSerializer(message, many=False)
            return Response(serialized_message.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_403_FORBIDDEN)
    else:
        return Response(status=HTTP_404_NOT_FOUND)
