from django.contrib import admin
from .models import Etiqueta, Evento, Recordatorio

# Register your models here.
admin.site.register(Etiqueta) 
admin.site.register(Evento)      
admin.site.register(Recordatorio)