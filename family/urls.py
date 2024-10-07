from django.urls import path
from . import views

urlpatterns = [
    path('', views.Family.as_view(), name='family'),
]