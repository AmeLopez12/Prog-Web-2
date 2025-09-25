from django.db import models

# Modelo para el manuscrito
class Manuscrito(models.Model):
    
    titulo = models.CharField(max_length=200)  # Titulo del manuscrit彼此
    autor = models.CharField(max_length=100)  # Autor del manuscrito
    resumen = models.TextField()  # Resumen del contenido
    aceptado = models.BooleanField(default=False)  # Estado de aceptacion
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de registro

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Manuscrito'
        verbose_name_plural = 'Manuscritos'

# Modelo para los archivos asociados al manuscrito
class ArchivoManuscrito(models.Model):
    manuscrito = models.ForeignKey(Manuscrito, on_delete=models.CASCADE, related_name='archivos')  # Relacion con Manuscrito
    archivo = models.FileField(upload_to='manuscritos/')  # Campo para archivo (PDF o imagen)

    def __str__(self):
        return f"Archivo de {self.manuscrito.titulo}"

    class Meta:
        verbose_name = 'Archivo de Manuscrito'
        verbose_name_plural = 'Archivos de Manuscritos'