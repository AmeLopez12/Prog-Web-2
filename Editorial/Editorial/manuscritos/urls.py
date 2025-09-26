from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaManuscritos.as_view(), name='lista_manuscritos'),
    path('registrar/', views.registrar_manuscrito, name='registrar_manuscrito'),
    path('actualizar/<int:pk>/', views.ActualizarManuscrito.as_view(), name='actualizar_manuscrito'),
    path('eliminar/<int:pk>/', views.EliminarManuscrito.as_view(), name='eliminar_manuscrito'),
    path('cambiar_estado/<int:pk>/', views.cambiar_estado, name='cambiar_estado'),
]