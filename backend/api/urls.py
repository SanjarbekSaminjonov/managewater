from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/v1/', views.overview, name='overview'),
    path('api/v1/basins/', include('api.basins.urls')),
    path('api/v1/users/', include('api.users.urls')),
]
