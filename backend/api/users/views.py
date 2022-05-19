from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def is_already_user(request):
    chat_id = request.data.get('chat_id')
    if chat_id is None:
        return Response(status=HTTP_400_BAD_REQUEST)
    if get_user_model().objects.filter(chat_id=chat_id).exists():
        return Response(status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    chat_id = request.data.get('chat_id')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    region = request.data.get('region')
    city = request.data.get('city')
    org_name = request.data.get('org_name')

    if all((username, password, chat_id, first_name, last_name, region, city, org_name)) \
            and not get_user_model().objects.filter(username=username).exists():

        get_user_model().objects.create_user(
            username=username,
            password=password,
            chat_id=chat_id,
            first_name=first_name,
            last_name=last_name,
            region=region,
            city=city,
            org_name=org_name
        )
        return Response(status=HTTP_201_CREATED)

    return Response(status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_user_chat_id(request):
    username = request.data.get('username')
    password = request.data.get('password')
    chat_id = request.data.get('chat_id')
    if all((username, password, chat_id)):
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(status=HTTP_404_NOT_FOUND)
        user.chat_id = chat_id
        user.save()
        return Response(status=HTTP_200_OK)
    return Response(status=HTTP_400_BAD_REQUEST)
