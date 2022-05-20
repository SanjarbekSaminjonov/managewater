from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE
)

from basins import models
from . import serializers

import datetime
import pytz


def get_timezone():
    return pytz.timezone('Asia/Tashkent')


def get_current_time():
    now = datetime.datetime.now(get_timezone())
    return now.strftime('%H:%M:%S %d/%m/%Y')


# @api_view(['POST'])
# def basin_create(request):
#     request_data = request.data
#     request_data['belong_to'] = request.user.id
#     serializer = serializers.BasinSerializer(data=request_data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(status=HTTP_201_CREATED)
#     basin_id = request_data.get('id')
#     if models.Basin.objects.filter(pk=basin_id).exists():
#         return Response(status=HTTP_400_BAD_REQUEST)
#     return Response(status=HTTP_406_NOT_ACCEPTABLE)


# @api_view(['GET'])
# def basins_list(request):
#     basins = models.Basin.objects.filter(belong_to=request.user)
#     serialized_basins = serializers.BasinSerializer(basins, many=True)
#     return Response(serialized_basins.data, status=HTTP_200_OK)


# @api_view(['GET'])
# def basin_detail(request, pk):
#     basin = models.Basin.objects.filter(
#         belong_to=request.user).filter(pk=pk).first()
#     if basin is not None:
#         serialized_basin = serializers.BasinSerializer(basin, many=False)
#         return Response(serialized_basin.data, status=HTTP_200_OK)
#     else:
#         return Response(status=HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# def basin_update(request, pk):
#     basin = models.Basin.objects.filter(
#         belong_to=request.user).filter(pk=pk).first()
#     if basin is not None:
#         basin.conf_height = request.data.get('conf_height')
#         basin.save()
#         return Response(status=HTTP_200_OK)
#     else:
#         return Response(status=HTTP_400_BAD_REQUEST)


##############################################################


@api_view(['POST'])
@permission_classes([AllowAny])
def basin_message_create(request):
    serializer = serializers.BasinMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        basin_id = request.data.get('basin')
        basin = models.Basin.objects.filter(pk=basin_id).first()
        basin.latitude = request.data.get('latitude')
        basin.longitude = request.data.get('longitude')
        basin.save()

        data = {
            'request': 'success',
            'height': basin.height + basin.conf_height,
            'phone': basin.phone,
            'datetime': get_current_time()
        }
        return Response(data, status=HTTP_201_CREATED)
    data = {
        'request': 'error',
    }
    return Response(data, status=HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def basin_messages_list(request):
#     messages = models.BasinMessage.objects.filter(
#         basin__belong_to=request.user)
#     serialized_messages = serializers.BasinMessageSerializer(
#         messages, many=True)
#     return Response(serialized_messages.data, status=HTTP_200_OK)


# @api_view(['GET'])
# def basin_message_detail(request, pk):
#     message = models.BasinMessage.objects.filter(pk=pk).first()
#     if message is not None:
#         if message.basin.belong_to == request.user:
#             serialized_message = serializers.BasinMessageSerializer(
#                 message, many=False)
#             return Response(serialized_message.data, status=HTTP_200_OK)
#         else:
#             return Response(status=HTTP_403_FORBIDDEN)
#     else:
#         return Response(status=HTTP_404_NOT_FOUND)
