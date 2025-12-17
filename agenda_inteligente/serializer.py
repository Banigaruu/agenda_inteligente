from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Evento, Etiqueta, Recordatorio, ESTADO_CHOICES


class EtiquetaSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(
        choices=Etiqueta.COLOR_CHOICES
    )
    color_display = serializers.CharField(
        source='get_color_display',
        read_only=True
    )

    class Meta:
        model = Etiqueta
        fields = [
            'id',
            'nombre',
            'color',
            'color_display',
        ]


class EventoSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(max_length=200, label='Título')
    descripcion = serializers.CharField(
        label='Descripción',
        required=False,
        allow_blank=True
    )

    fecha_inicio = serializers.DateTimeField(label='Fecha Inicio')
    fecha_fin = serializers.DateTimeField(label='Fecha Fin')

    estado = serializers.ChoiceField(
        choices=ESTADO_CHOICES,
        label='Estado'
    )

    etiquetas = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    id_etiquetas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Etiqueta.objects.all(),
        source='etiquetas'
    )

    class Meta:
        model = Evento
        fields = [
            'id',
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'id_etiquetas',
            'etiquetas',
            'fecha_creacion',
            'ultima_modificacion',
        ]
def validate(self, data):
    usuario = self.context['request'].user
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')

    eventos_solapados = Evento.objects.filter(
        usuario=usuario,
        fecha_inicio__lt=fecha_fin,
        fecha_fin__gt=fecha_inicio
    )

    if self.instance:
        eventos_solapados = eventos_solapados.exclude(
            id=self.instance.id
        )

    if eventos_solapados.exists():
        raise serializers.ValidationError(
            'El evento se solapa con otro evento existente.'
        )

    return data

class RecordatorioSerializer(serializers.ModelSerializer):
    fecha_recordatorio = serializers.DateTimeField(
        label='Fecha Recordatorio'
    )
    enviado = serializers.BooleanField(
        label='Enviado',
        read_only=True
    )

    evento = serializers.StringRelatedField(
        read_only=True
    )
    id_evento = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.all(),
        source='evento'
    )

    class Meta:
        model = Recordatorio
        fields = [
            'id',
            'fecha_recordatorio',
            'enviado',
            'id_evento',
            'evento',
        ]