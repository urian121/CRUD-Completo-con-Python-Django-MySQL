from django.shortcuts import render, redirect
from decimal import Decimal  # Asegúrate de importar Decimal
from django.contrib import messages  # Para usar mensajes flash
from django.core.exceptions import ObjectDoesNotExist
from . models import Empleado  # Importando el modelo de Empleado


def inicio(request):
    opciones_edad = [(str(edad), str(edad)) for edad in range(18, 51)]
    data = {
        'opciones_edad': opciones_edad,
    }
    return render(request, 'empleado/form_empleado.html', data)


def registrar_empleado(request):
    data = {}  # Inicializa un diccionario vacio de data
    if request.method == 'POST':
        nombre = request.POST.get('nombre_empleado')
        apellido = request.POST.get('apellido_empleado')
        email = request.POST.get('email_empleado')
        edad = request.POST.get('edad_empleado')
        genero = request.POST.get('genero_empleado')
        salario = request.POST.get('salario_empleado')

        # Obtén la imagen del formulario
        foto_empleado = request.FILES.get('foto_empleado')

        # Procesa los datos y guarda en la base de datos (ejemplo)
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
            request, f"Felicitaciones, el empleado { nombre } fue registrado correctamente  😉")
        return redirect('listar_empleados')

    # Si no se ha enviado el formulario, simplemente renderiza la plantilla con el formulario vacío
    return render(request, 'empleado/form_empleado.html', data)


def listar_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los registros de empleados
    data = {
        'empleados': empleados,
    }
    return render(request, 'empleado/lista_empleados.html', data)


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


def detalles_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
        data = {"empleado": empleado}
        return render(request, "empleado/detalles.html", data)
    except Empleado.DoesNotExist:
        error_message = f"no existe ningún registro para la busqueda id: {id}"
        return render(request, "empleado/lista_empleados.html", {"error_message": error_message})


def actualizar_empleado(request, id):
    try:
        if request.method == "POST":
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

            # Verifica si se proporciona una imagen en la solicitud POST
            if 'foto_empleado' in request.FILES:
                # Actualiza la imagen solo si se proporciona en la solicitud
                empleado.foto_empleado = request.FILES['foto_empleado']

            empleado.save()
        return redirect('listar_empleados')
    except ObjectDoesNotExist:
        error_message = f"El Empleado con id: {id} no se actualizó."
        return render(request, "empleado/lista_empleados.html", {"error_message": error_message})
