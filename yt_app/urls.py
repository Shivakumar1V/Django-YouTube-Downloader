from django.urls import path
from yt_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('getvideo/', views.getVideo, name='getVideo'),
    path('download/', views.downloadVid, name='downloadVid'),
]
