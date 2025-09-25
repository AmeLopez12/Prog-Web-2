from django.db import models
from django.core.validators import FileExtensionValidator

# Modelo principal (un envio/manuscrito)
class Poll(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=100, verbose_name="Autor")
    abstract = models.TextField(verbose_name="Resumen", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return f"{self.title} - {self.author}"

# Modelo archivo asociado al envío
class PollFile(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(
        upload_to="polls_files/",  # se guardarán en MEDIA_ROOT/polls_files/
        validators=[FileExtensionValidator(allowed_extensions=["pdf","jpg","jpeg","png","gif"])],
        verbose_name="Archivo"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")

    def __str__(self):
        return self.file.name
