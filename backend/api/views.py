from django.shortcuts import redirect
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


def home(request):
    return redirect('admin/')


@api_view(['GET'])
@permission_classes([AllowAny])
def overview(request):
    url = 'https://managewater.pythonanywhere.com/api/v1/'

    if settings.DEBUG:
        url = 'http://127.0.0.1:8000/api/v1/'

    urls_map = {
        'API url': url,

        'Users': {
            'Check': url + 'users/check/',
            'Create': url + 'users/create/',
            'Update': url + 'users/update/'
        },

        'Basins': {
            'List': url + 'basins/all/',
            'Create': url + 'basins/create/',
            'Detail': url + 'basins/basin_id/',
        },

        'Basin messages': {
            'Message List': url + 'basins/messages/all/',
            'Message Create': url + 'basins/messages/create/',
            'Message Detail': url + 'basins/messages/message_id/',
        },
    }

    return Response(urls_map)
