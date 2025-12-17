from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.views import LoginView
from .models import Evento, Etiqueta, Recordatorio
from .serializer import (
    EventoSerializer,
    EtiquetaSerializer,
    RecordatorioSerializer
)
from .filters import EventoFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, 'home/index.html')

class LoginViewPersonalizado(LoginView):
    template_name = 'registration/login.html'

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    # Filtros
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoFilter

    def get_queryset(self):
        return Evento.objects.filter(
            usuario=self.request.user
        ).order_by('fecha_inicio')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Etiqueta.objects.filter(
            usuario=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class RecordatorioViewSet(viewsets.ModelViewSet):
    queryset = Recordatorio.objects.all()
    serializer_class = RecordatorioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recordatorio.objects.filter(
            evento__usuario=self.request.user
        ).order_by('fecha_recordatorio')
