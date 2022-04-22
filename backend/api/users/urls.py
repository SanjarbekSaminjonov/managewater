from django.urls import path
from . import views


urlpatterns = [
    path('is-already-user/', views.is_already_user),
    path('check/', views.check_user),
    path('create/', views.create_user),
    path('change-username/', views.change_user_username),
]
