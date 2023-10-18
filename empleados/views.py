from django.shortcuts import render, redirect
from django.contrib import messages  # Para usar mensajes flash
from . models import Empleado  # Importando el modelo de Empleado


def inicio(request):
    opciones_edad = [(str(edad), str(edad)) for edad in range(18, 51)]
    data = {
        'opciones_edad': opciones_edad,
    }
    return render(request, 'form_empleado.html', data)


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
    return render(request, 'formulario_libro.html', data)


def listar_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los registros de empleados
    data = {
        'empleados': empleados,
    }
    return render(request, 'lista_empleados.html', data)
