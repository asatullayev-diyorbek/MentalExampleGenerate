from django.urls import path
from . import views

urlpatterns = [
    path('', views.Menu.as_view(), name='menu'),
    path('small-friends/', views.SmallFriends.as_view(), name='smallFriends'),

    path('download/<int:file_id>/', views.download_pdf, name='download'),
]
