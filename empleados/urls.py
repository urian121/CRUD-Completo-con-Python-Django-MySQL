from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar_empleado/', views.registrar_empleado,
         name='registrar_empleado'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
]
