from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_manuscrito, name='registrar_manuscrito'),
    path('', views.ListaManuscritos.as_view(), name='lista_manuscritos'),
    path('editar/<int:pk>/', views.ActualizarManuscrito.as_view(), name='actualizar_manuscrito'),
    path('eliminar/<int:pk>/', views.EliminarManuscrito.as_view(), name='eliminar_manuscrito'),
    path('estado/<int:pk>/', views.cambiar_estado, name='cambiar_estado'),
]