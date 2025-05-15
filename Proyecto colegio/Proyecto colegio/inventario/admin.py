from django.contrib import admin
from django.utils.html import format_html
from .models import Inventario

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    readonly_fields = ('codigo_barras_preview',)

    list_display = (
        'equipo', 'tipo_equipo', 'marca', 'modelo',
        'ubicacion', 'estado', 'fondo_adquisicion', 'codigo_barras_preview',
        'prestamo_activo', 'nombre_solicitante'
    )

    list_filter = (
        'tipo_equipo', 'estado', 'ubicacion', 'fondo_adquisicion', 'prestamo_activo'
    )
    search_fields = (
        'equipo', 'marca', 'modelo', 'codigo', 'nombre_solicitante'
    )

    fieldsets = (
        ('Información del equipo', {
            'fields': (
                'equipo', 'tipo_equipo', 'marca', 'modelo',
                'ubicacion', 'estado', 'foto',
            )
        }),
        ('Código de Barras', {
            'fields': (
                'codigo_barras_preview',
            )
        }),
        ('Información de préstamo', {
            'fields': (
                'prestamo_activo', 'nombre_solicitante',
                'fecha_inicio_prestamo', 'fecha_fin_prestamo',
            )
        }),
        ('Información de adquisición', {
            'fields': (
                'fondo_adquisicion', 'fecha_adquisicion',
            )
        }),
    )

    def codigo_barras_preview(self, obj):
        if obj.codigo_barras:
            return format_html('<img src="{}" width="150" />', obj.codigo_barras.url)
        return "No generado"
    codigo_barras_preview.short_description = "Código de Barras"
