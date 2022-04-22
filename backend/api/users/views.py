from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED

from .serializers import CustomUserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def is_already_user(request):
    username = request.data.get('username')

    if username is None:
        return Response({'error': 'Please provide username'}, status=HTTP_400_BAD_REQUEST)

    user = get_user_model().objects.filter(username=username).first()

    if not user:
        return Response(
            {
                'error': 'Not found'
            },
            status=HTTP_404_NOT_FOUND
        )

    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_user(request):
    secret_key = request.data.get('secret_key')
    if secret_key is None or secret_key.strip() == '':
        return Response(
            {
                'error': 'Please provide a secret_key'
            },
            status=HTTP_400_BAD_REQUEST
        )

    pk, username = secret_key.split('#')

    user = get_user_model().objects.filter(pk=pk).filter(username=username).first()
    if not user:
        return Response(
            {
                'error': 'Not found'
            },
            status=HTTP_404_NOT_FOUND
        )

    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        print(serializer)
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        region = request.data.get('region')
        city = request.data.get('city')
        org_name = request.data.get('org_name')
        password = username[::-1]

        user = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            region=region,
            city=city,
            org_name=org_name,
            password=password
        )
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data, status=HTTP_201_CREATED)

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_user_username(request):
    secret_key = request.data.get('secret_key')
    new_username = request.data.get('username')
    password = new_username[::-1]

    if secret_key is None or secret_key.strip() == '':
        return Response(
            {
                'error': 'Please provide a secret_key'
            },
            status=HTTP_400_BAD_REQUEST
        )

    pk, username = secret_key.split('#')
    user = get_user_model().objects.filter(pk=pk).filter(username=username).first()

    if user is None:
        return Response({'error': 'Secret key is not true'}, status=HTTP_400_BAD_REQUEST)
    else:
        user.username = new_username
        user.set_password(password)
        user.save()
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data, status=HTTP_200_OK)
