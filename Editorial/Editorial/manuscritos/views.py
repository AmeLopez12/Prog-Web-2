from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Manuscrito, ArchivoManuscrito
from .forms import ManuscritoForm, ArchivoForm

def registrar_manuscrito(request):
    if request.method == 'POST':
        formulario_manuscrito = ManuscritoForm(request.POST)
        formulario_archivos = ArchivoForm(request.POST, request.FILES)
        if formulario_manuscrito.is_valid() and formulario_archivos.is_valid():
            manuscrito = formulario_manuscrito.save()
            archivos = formulario_archivos.cleaned_data['archivos']  # Lista de archivos validados
            for archivo in archivos:
                archivo_instance = ArchivoManuscrito(manuscrito=manuscrito, archivo=archivo)
                archivo_instance.save()
            return redirect('lista_manuscritos')
        else:
            for field, errors in formulario_archivos.errors.items():
                if field != '__all__':
                    for error in errors:
                        print(f"Error en {field}: {error}")
    else:
        formulario_manuscrito = ManuscritoForm()
        formulario_archivos = ArchivoForm()
    return render(request, 'manuscritos/registrar_manuscrito.html', {
        'formulario_manuscrito': formulario_manuscrito,
        'formulario_archivos': formulario_archivos
    })
    
# Vista para listar manuscritos
class ListaManuscritos(ListView):
    model = Manuscrito
    template_name = 'manuscritos/lista_manuscritos.html'
    context_object_name = 'manuscritos'

# Vista para actualizar manuscrito
class ActualizarManuscrito(UpdateView):
    model = Manuscrito
    form_class = ManuscritoForm
    template_name = 'manuscritos/actualizar_manuscrito.html'
    success_url = reverse_lazy('lista_manuscritos')

# Vista para eliminar manuscrito
class EliminarManuscrito(DeleteView):
        model = Manuscrito
        template_name = 'manuscritos/eliminar_manuscrito.html'
        success_url = reverse_lazy('lista_manuscritos')

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            # Eliminar archivos asociados individualmente
            for archivo in self.object.archivos.all():
                archivo.delete()
            self.object.delete()
            return redirect(self.get_success_url())

# Vista para cambiar el estado de aceptacion
def cambiar_estado(request, pk):
    manuscrito = get_object_or_404(Manuscrito, pk=pk)
    if request.method == 'POST':
        manuscrito.aceptado = not manuscrito.aceptado  # Cambiar estado
        manuscrito.save()
        return redirect('lista_manuscritos')
    return render(request, 'manuscritos/cambiar_estado.html', {'manuscrito': manuscrito})