from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/v1/', views.overview, name='overview'),
    path('api/v1/basins/', include('api.basins.urls')),
    path('api/v1/users/', include('api.users.urls')),
]
