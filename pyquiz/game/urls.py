from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('game/<str:room_name>/', views.game),
]
