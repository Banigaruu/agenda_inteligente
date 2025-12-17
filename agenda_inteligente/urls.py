from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, EtiquetaViewSet, RecordatorioViewSet

router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'etiquetas', EtiquetaViewSet, basename='etiqueta')
router.register(r'recordatorios', RecordatorioViewSet, basename='recordatorio')

urlpatterns = [
    path('', include(router.urls)),
]
