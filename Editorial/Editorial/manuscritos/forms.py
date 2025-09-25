from django import forms
from .models import Manuscrito

# Formulario para el manuscrito
class ManuscritoForm(forms.ModelForm):
    class Meta:
        model = Manuscrito
        fields = ['titulo', 'autor', 'resumen']  # Campos a incluir
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'resumen': 'Resumen',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }