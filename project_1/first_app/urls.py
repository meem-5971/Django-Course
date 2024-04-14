from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about),
    path('courses/',views.courses),
    path("",views.home),
   
]
