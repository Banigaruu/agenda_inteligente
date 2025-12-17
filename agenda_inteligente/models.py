from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


ESTADO_CHOICES = (
    ('PENDIENTE', 'Pendiente'),
    ('COMPLETADO', 'Completado'),
    ('CANCELADO', 'Cancelado'),
)

class Etiqueta(models.Model):
    COLOR_CHOICES = (
    ('CELESTE', 'Celeste'),
    ('VERDE', 'Verde'),
    ('ROSA', 'Rosa'),
    ('MORADO', 'Morado'),
    ) 
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='etiquetas',
        null=True,
        blank=True
    )
    nombre = models.CharField(
        max_length=50,
        unique=True
    )
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='ROSA'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )
    etiquetas = models.ManyToManyField(
        Etiqueta,
        blank=True,
        related_name='eventos'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha_inicio']

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError(
                    'La fecha de inicio debe ser anterior a la fecha de fin.'
                )


class Recordatorio(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='recordatorios'
    )
    fecha_recordatorio = models.DateTimeField()
    enviado = models.BooleanField(default=False)
    mensaje = models.CharField(
        max_length=255,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Recordatorio para {self.evento.titulo}'
