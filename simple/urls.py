from django.urls import path
from . import views

urlpatterns = [
    path('', views.Simple.as_view(), name='simple'),
]