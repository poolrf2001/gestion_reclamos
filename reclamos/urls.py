from django.urls import path
from . import views

urlpatterns = [
    path('consulta/', views.consulta_reclamo, name='consulta_reclamo'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('limpiar_sesion/', views.limpiar_sesion, name='limpiar_sesion'),
]
