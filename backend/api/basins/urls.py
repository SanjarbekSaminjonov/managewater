from django.urls import path

from . import views


urlpatterns = [
    path('messages/create/', views.BasinMessageCreateAPIView.as_view()),
    path('messages/all/', views.basin_messages_list),
    path('messages/<int:pk>/', views.basin_message_detail),

    path('create/', views.BasinCreateAPIView.as_view()),
    path('all/', views.basins_list),
    path('<str:pk>/', views.basin_detail),
]
