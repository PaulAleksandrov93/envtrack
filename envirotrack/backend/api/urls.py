from django.urls import path
from . import views
from . views import MyTokenObtainPairView


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('parameters/', views.getEnviromentalParameters, name='all_parameters'),
    path('parameters/create/', views.createEnvironmentalParameters, name='create-environmental-parameters'),
    path('parameters/<str:pk>/', views.getEnviromentalParameter, name="parameterlist"),
    path('current_user/', views.get_current_user),

    
    path('parameters/update/<str:pk>/', views.updateEnvironmentalParameters, name='update-environmental-parameters'),
    path('parameters/delete/<str:pk>/', views.deleteEnvironmentalParameters, name='delete-environmental-parameters'),
    path('rooms/', views.getRooms, name='room-list'),  

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('measurement_instruments/', views.getMeasurementInstruments, name='measurement-instruments-list'),
    # path('parameters/filter/', views.filterEnvironmentalParameters, name='filter-environmental-parameters'),
    
    path('responsibles/', views.getResponsibles, name='responsibles-list'),
    path('parameter_sets/', views.getParameterSets, name='parameter-set-list'),  
    path('parameter_sets/create/', views.createParameterSet, name='create-parameter-set'),
    path('parameter_sets/<str:pk>/', views.getParameterSet, name="parameter-set-detail"),
    path('parameter_sets/update/<str:pk>/', views.updateParameterSet, name='update-parameter-set'),
    path('parameter_sets/delete/<str:pk>/', views.deleteParameterSet, name='delete-parameter-set'),
    path('export-parameters/', views.export_parameters_to_excel, name='export_parameters'),
]
