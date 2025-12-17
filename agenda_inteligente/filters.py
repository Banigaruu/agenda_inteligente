import django_filters
from .models import Evento, Etiqueta


class EventoFilter(django_filters.FilterSet):

    estado = django_filters.ChoiceFilter(
        choices=Evento._meta.get_field('estado').choices,
        label='Estado'
    )

    etiquetas = django_filters.ModelChoiceFilter(
        queryset=Etiqueta.objects.all(),
        label='Etiqueta'
    )

    fecha_inicio = django_filters.DateFilter(
        field_name='fecha_inicio',
        lookup_expr='date',
        label='Fecha de inicio'
    )

    fecha_fin = django_filters.DateFilter(
        field_name='fecha_fin',
        lookup_expr='date',
        label='Fecha de fin'
    )

    class Meta:
        model = Evento
        fields = [
            'estado',
            'etiquetas',
            'fecha_inicio',
            'fecha_fin',
        ]
