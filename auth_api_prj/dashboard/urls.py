from django.urls import path
from .views import DashBoardHome


urlpatterns = [
    
    path('home-dashboard/',DashBoardHome.as_view(), name="home")
  
]
