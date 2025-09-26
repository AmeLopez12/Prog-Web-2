from django import forms
from .models import Manuscrito
import os

class ManuscritoForm(forms.ModelForm):
    class Meta:
        model = Manuscrito
        fields = ['titulo', 'autor', 'resumen']
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

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultiFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png,.gif'
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return []
        if isinstance(data, list):
            files = []
            for file_data in data:
                file = super().clean(file_data, initial)
                files.append(file)
            return files
        else:
            file = super().clean(data, initial)
            return [file]

    def to_python(self, data):
        if isinstance(data, (list, tuple)):
            files = []
            for file_data in data:
                file = super().to_python(file_data)
                files.append(file)
            return files
        return super().to_python(data)

    def validate(self, data):
        super().validate(data)
        if isinstance(data, (list, tuple)):
            for file in data:
                if file is None:
                    continue

class ArchivoForm(forms.Form):
    archivos = MultipleFileField(
        required=True,
        error_messages={
            'required': 'Debes seleccionar al menos un archivo antes de registrar el manuscrito.',
        },
        help_text='Puedes seleccionar varios archivos al mismo tiempo manteniendo presionada la tecla Ctrl (o Cmd en Mac).'
    )

    def clean_archivos(self):
        archivos = self.cleaned_data.get('archivos', [])
        if not archivos:
            raise forms.ValidationError("Debes subir al menos un archivo.")

        valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'gif']
        for archivo in archivos:
            if not archivo:
                continue
            name, ext = os.path.splitext(archivo.name)
            extension = ext.lower().lstrip('.')  # e.g., 'pdf'
            if extension not in valid_extensions:
                raise forms.ValidationError(
                    f"El archivo '{archivo.name}' no tiene un formato permitido. "
                    f"Formatos válidos: {', '.join(valid_extensions)}"
                )
            if archivo.size == 0:
                raise forms.ValidationError(
                    f"El archivo '{archivo.name}' está vacío. Por favor, selecciona otro."
                )
            valid_mimes = {
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif'
            }
            if extension in valid_mimes and archivo.content_type != valid_mimes[extension]:
                raise forms.ValidationError(
                    f"El archivo '{archivo.name}' parece no ser un {extension.upper()} válido (tipo MIME: {archivo.content_type})."
                )
        return archivos