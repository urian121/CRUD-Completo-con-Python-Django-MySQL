from django.shortcuts import render, redirect
import os
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile

from decimal import Decimal  # Asegúrate de importar Decimal
from django.contrib import messages  # Para usar mensajes flash
from django.core.exceptions import ObjectDoesNotExist

# Para el informe (Reporte) Excel
import pandas as pd

import json

import logging

from django.utils import timezone
from openpyxl import Workbook  # Para generar el informe en excel
from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404
from . models import Empleado  # Importando el modelo de Empleado


def inicio(request):
    opciones_edad = [(str(edad), str(edad)) for edad in range(18, 51)]
    data = {
        'opciones_edad': opciones_edad,
    }
    return render(request, 'empleado/form_empleado.html', data)


def listar_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los registros de empleados
    data = {
        'empleados': empleados,
    }
    return render(request, 'empleado/lista_empleados.html', data)


def view_form_carga_masiva(request):
    return render(request, 'empleado/form_carga_masiva.html')


def detalles_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
        data = {"empleado": empleado}
        return render(request, "empleado/detalles.html", data)
    except Empleado.DoesNotExist:
        error_message = f"no existe ningún registro para la busqueda id: {id}"
        return render(request, "empleado/lista_empleados.html", {"error_message": error_message})


def registrar_empleado(request):
    if request.method == 'POST':
        """ 
        Iterando a través de todos los elementos en el diccionario request.POST, 
        que contiene los datos enviados a través del método POST, e imprime cada par clave-valor en la consola
        for key, value in request.POST.items():
            print(f'{key}: {value}')
        """
        nombre = request.POST.get('nombre_empleado')
        apellido = request.POST.get('apellido_empleado')
        email = request.POST.get('email_empleado')
        edad = request.POST.get('edad_empleado')
        genero = request.POST.get('genero_empleado')
        salario = request.POST.get('salario_empleado')

        # Obtén la imagen del formulario
        foto_empleado = request.FILES.get('foto_empleado')

        if foto_empleado:
            foto_empleado = generate_unique_filename(foto_empleado)

        # Procesa los datos y guarda en la base de datos
        empleado = Empleado(
            nombre_empleado=nombre,
            apellido_empleado=apellido,
            email_empleado=email,
            edad_empleado=edad,
            genero_empleado=genero,
            salario_empleado=salario,
            foto_empleado=foto_empleado,
        )
        empleado.save()

        messages.success(
            request, f"Felicitaciones, el empleado {nombre} fue registrado correctamente 😉")
        return redirect('listar_empleados')

    # Si no se ha enviado el formulario, simplemente renderiza la plantilla con el formulario vacío
    return redirect('inicio')


def view_form_update_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
        opciones_edad = [(int(edad), int(edad)) for edad in range(18, 51)]

        data = {"empleado": empleado,
                'opciones_edad': opciones_edad,
                }
        return render(request, "empleado/form_update_empleado.html", data)
    except ObjectDoesNotExist:
        error_message = f"El Empleado con id: {id} no existe."
        return render(request, "empleado/lista_empleados.html", {"error_message": error_message})


def actualizar_empleado(request, id):
    try:
        if request.method == "POST":
            # Obtén el empleado existente
            empleado = Empleado.objects.get(id=id)

            empleado.nombre_empleado = request.POST.get('nombre_empleado')
            empleado.apellido_empleado = request.POST.get('apellido_empleado')
            empleado.email_empleado = request.POST.get('email_empleado')
            empleado.edad_empleado = int(request.POST.get('edad_empleado'))
            empleado.genero_empleado = request.POST.get('genero_empleado')

            # Convierte el valor a Decimal
            salario_empleado = Decimal(request.POST.get(
                'salario_empleado').replace(',', '.'))
            empleado.salario_empleado = salario_empleado

            if 'foto_empleado' in request.FILES:
                # Actualiza la imagen solo si se proporciona en la solicitud
                empleado.foto_empleado = generate_unique_filename(
                    request.FILES['foto_empleado'])

            empleado.save()
        return redirect('listar_empleados')
    except ObjectDoesNotExist:
        error_message = f"El Empleado con id: {id} no se actualizó."
        return render(request, "empleado/lista_empleados.html", {"error_message": error_message})


def informe_empleado(request):
    try:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="data_empleados.xlsx"'

        # Consulta la base de datos para obtener los datos que deseas exportar
        datos = Empleado.objects.all()

        # Crea un nuevo libro de Excel y una hoja de trabajo
        workbook = Workbook()
        worksheet = workbook.active

        # Agrega encabezados
        worksheet.append(
            ['Nombre del Empleado', 'Apellido del Empleado', 'Edad del Empleado', 'Sexo del Empleado', 'Email del Empleado', 'Salario del Empleado', 'Fecha de Registro'])

        # Agrega los datos a la hoja de trabajo
        for dato in datos:
            worksheet.append([dato.nombre_empleado, dato.apellido_empleado, dato.edad_empleado,
                              dato.genero_empleado, dato.email_empleado, dato.salario_empleado, dato.created_at.astimezone(timezone.utc).replace(tzinfo=None)])

        # Guarda el libro de Excel en la respuesta HTTP
        workbook.save(response)

        return response
    except ObjectDoesNotExist:
        error_message = "El Empleado con id: {id} no existe."
        return render(request, "empleado/lista_empleados.html", {"error_message": error_message})


def eliminar_empleado(request):
    if request.method == 'POST':
        id_empleado = json.loads(request.body)['idEmpleado']
        # Busca el empleado por su ID
        empleado = get_object_or_404(Empleado, id=id_empleado)
        # Realiza la eliminación del empleado
        empleado.delete()
        return JsonResponse({'resultado': 1})
    return JsonResponse({'resultado': 1})


def cargar_archivo(request):
    try:
        if request.method == 'POST':
            archivo_xlsx = request.FILES['archivo_xlsx']
            if archivo_xlsx.name.endswith('.xlsx'):
                df = pd.read_excel(archivo_xlsx, header=0)

                for _, row in df.iterrows():
                    nombre_empleado = row['Nombre']
                    apellido_empleado = row['Apellido']
                    edad_empleado = row['Edad']
                    email_empleado = row['Email']
                    genero_empleado = row['Sexo']
                    salario_empleado = row['Salario']

                    empleado, creado = Empleado.objects.update_or_create(
                        email_empleado=email_empleado,
                        defaults={
                            'nombre_empleado': nombre_empleado,
                            'apellido_empleado': apellido_empleado,
                            'edad_empleado': edad_empleado,
                            'email_empleado': email_empleado,
                            'genero_empleado': genero_empleado,
                            'salario_empleado': salario_empleado,
                            'foto_empleado': '',
                        }
                    )

                return JsonResponse({'status_server': 'success', 'message': 'Los datos se importaron correctamente.'})
            else:
                return JsonResponse({'status_server': 'error', 'message': 'El archivo debe ser un archivo de Excel válido.'})
        else:
            return JsonResponse({'status_server': 'error', 'message': 'Método HTTP no válido.'})

    except Exception as e:
        logging.error("Error al cargar el archivo: %s", str(e))
        return JsonResponse({'status_server': 'error', 'message': f'Error al cargar el archivo: {str(e)}'})


# Genera un nombre único para el archivo utilizando UUID y conserva la extensión.
def generate_unique_filename(file):
    extension = os.path.splitext(file.name)[1]
    unique_name = f'{uuid.uuid4()}{extension}'
    return SimpleUploadedFile(unique_name, file.read())
