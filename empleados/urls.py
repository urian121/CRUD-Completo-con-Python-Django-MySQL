from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar-nuevo-empleado/', views.registrar_empleado,
         name='registrar_empleado'),
    path('lista-de-empleados/', views.listar_empleados, name='listar_empleados'),

    path('detalles-del-empleado/<str:id>/',
         views.detalles_empleado, name='detalles_empleado'),

    path('formulario-para-actualizar-empleado/<str:id>/',
         views.view_form_update_empleado, name='view_form_update_empleado'),

    path('actualizar-empleado/<str:id>/',
         views.actualizar_empleado, name='actualizar_empleado'),
    path('eliminar-empleado/', views.eliminar_empleado, name='eliminar_empleado'),


    path('descargar-informe-empleados',
         views.informe_empleado, name="informe_empleado"),
    path('formulario-para-la-carga-masiva-de-empleados',
         views.view_form_carga_masiva, name="view_form_carga_masiva"),
    path('subir-data-xlsx', views.cargar_archivo, name="cargar_archivo"),

]
