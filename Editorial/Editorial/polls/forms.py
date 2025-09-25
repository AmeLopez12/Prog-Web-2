from django import forms
from .models import Poll

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PollForm(forms.ModelForm):
    attachments = forms.FileField(
        widget=MultiFileInput(attrs={
            'multiple': True,
            'accept': 'application/pdf,image/*'
        }),
        required=True,
        label="Archivos (PDF o imágenes)"
    )

    class Meta:
        model = Poll
        fields = ['title', 'author', 'abstract']
        labels = {
            'title': 'Título del Manuscrito',
            'author': 'Autor',
            'abstract': 'Resumen',
        }