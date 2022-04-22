from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from basins import models
from . import serializers


class BasinCreateAPIView(generics.CreateAPIView):
    queryset = models.Basin.objects.all()
    serializer_class = serializers.BasinSerializer


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
            return Response({'error': 'This basin does not belong to you'}, status=HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Basin not found'}, status=HTTP_404_NOT_FOUND)


##############################################################


class BasinMessageCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = models.BasinMessage.objects.all()
    serializer_class = serializers.BasinMessageSerializer


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
            return Response({'error': 'This message does not belong to you'}, status=HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Basin message not found'}, status=HTTP_404_NOT_FOUND)
