# Registro de modelos en el admin
from django.contrib import admin
from .models import Manuscrito, ArchivoManuscrito

admin.site.register(Manuscrito)
admin.site.register(ArchivoManuscrito)