from django.urls import path
from . import views


urlpatterns = [
    # path('check/', views.is_already_user),
    path('create/', views.create_user),
    # path('update/', views.change_user_chat_id),
]
