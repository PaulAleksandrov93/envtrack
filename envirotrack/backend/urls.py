from django.urls import path
from . import views

urlpatterns = [
    path('parameters/', views.getEnviromentalParameters, name="parameterslist"),
    path('parameters/<str:pk>/', views.getEnviromentalParameter, name="parameterlist"),
    path('parameters/create/', views.createEnvironmentalParameters, name='create-environmental-parameters'),
    path('parameters/update/<str:pk>/', views.updateEnvironmentalParameters, name='update-environmental-parameters'),
    path('parameters/delete/<str:pk>/', views.deleteEnvironmentalParameters, name='delete-environmental-parameters'),
    path('rooms/', views.getRooms, name='room-list'),  # Добавлен URL для получения списка комнат
    path('current_user/', views.get_current_user),
    
]
