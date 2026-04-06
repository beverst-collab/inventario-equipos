# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import date

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_equipo = models.CharField(max_length=100, default="N/A")
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, default="N/A")
    serial = models.CharField(max_length=100, default="N/A")
    cantidad = models.IntegerField(default=1)
    estado = models.CharField(max_length=50, default="activo")
    fecha_registro = models.DateField(default=date.today)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre