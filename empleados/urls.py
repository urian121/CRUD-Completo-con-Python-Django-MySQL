from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar_empleado/', views.registrar_empleado,
         name='registrar_empleado'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),

    path('detalles-del-empleado/<str:id>/',
         views.detalles_empleado, name='detalles_empleado'),

    path('formulario-para-actualizar-empleado/<str:id>/',
         views.view_form_update_empleado, name='view_form_update_empleado'),

    path('actualizar-empleado/<str:id>/',
         views.actualizar_empleado, name='actualizar_empleado'),

]
