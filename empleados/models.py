from django.db import models

# Definir una tupla con los valores del select genero_empleado
generos = (
    ("Masculino", "Masculino"),
    ("Femenino", "Femenino"),
    ("Otro", "Otro"),
)


class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=200)
    apellido_empleado = models.CharField(max_length=100)
    email_empleado = models.EmailField(max_length=50)
    edad_empleado = models.IntegerField()
    genero_empleado = models.CharField(max_length=80, choices=generos)
    salario_empleado = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    foto_empleado = models.ImageField(
        upload_to='fotos_empleados/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def es_extension_valida(self):
        extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif']
        return any(self.foto_empleado.name.lower().endswith(ext) for ext in extensiones_validas)

    """ la clase Meta dentro de un modelo se utiliza para proporcionar metadatos adicionales sobre el modelo."""
    class Meta:
        db_table = "empleados"
        ordering = ['-created_at']
