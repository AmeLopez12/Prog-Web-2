from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Manuscrito, ArchivoManuscrito
from .forms import ManuscritoForm
from django.forms import formset_factory

# Vista para registrar un manuscrito
def registrar_manuscrito(request):
    if request.method == 'POST':
        formulario_manuscrito = ManuscritoForm(request.POST)
        if formulario_manuscrito.is_valid():
            manuscrito = formulario_manuscrito.save()  # Guardar manuscrito
            # Manejar multiples archivos desde request.FILES
            archivos_subidos = request.FILES.getlist('archivos')
            for archivo_subido in archivos_subidos:
                if archivo_subido:
                    archivo = ArchivoManuscrito(manuscrito=manuscrito, archivo=archivo_subido)
                    archivo.save()  # Guardar cada archivo
            return redirect('lista_manuscritos')
    else:
        formulario_manuscrito = ManuscritoForm()
    return render(request, 'manuscritos/registrar_manuscrito.html', {
        'formulario_manuscrito': formulario_manuscrito
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
            print(f"Manuscrito a eliminar: {self.object.titulo}")
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