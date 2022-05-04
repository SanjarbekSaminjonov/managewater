from django.urls import path

from . import views


urlpatterns = [
    path('messages/create/', views.basin_message_create),
    path('messages/all/', views.basin_messages_list),
    path('messages/<int:pk>/', views.basin_message_detail),

    path('create/', views.basin_create),
    path('all/', views.basins_list),
    path('<str:pk>/', views.basin_detail),
    path('<str:pk>/update/', views.basin_update),
]
