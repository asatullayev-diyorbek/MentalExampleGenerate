from django.urls import path
from . import views

urlpatterns = [
    path('', views.BigFriends.as_view(), name='BigFriends'),
]