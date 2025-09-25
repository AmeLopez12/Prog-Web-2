import os
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
    manuscrito = models.ForeignKey(Manuscrito, related_name='archivos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='manuscritos/')

    def __str__(self):
        return f"Archivo de {self.manuscrito.titulo}"

    def delete(self, *args, **kwargs):
        # Eliminar el archivo del sistema de archivos antes de eliminar la entrada
        if self.archivo:
            try:
                if os.path.isfile(self.archivo.path):
                    os.remove(self.archivo.path)
                    print(f"Archivo eliminado con éxito: {self.archivo.path}")
                else:
                    print(f"Archivo no encontrado en: {self.archivo.path}")
            except Exception as e:
                print(f"Error al eliminar archivo: {e}")
        super().delete(*args, **kwargs)
    class Meta:
        verbose_name = 'Archivo de Manuscrito'
        verbose_name_plural = 'Archivos de Manuscritos'
    
