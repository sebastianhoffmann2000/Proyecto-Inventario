from django.core.management.base import BaseCommand
from inventario.models import Inventario

class Command(BaseCommand):
    help = 'Limpia y normaliza los datos de tipo_equipo, ubicación y estado'

    def handle(self, *args, **kwargs):
        actualizados = 0
        for equipo in Inventario.objects.all():
            original = (equipo.tipo_equipo, equipo.ubicacion, equipo.estado)

            # Limpiar y aplicar formato
            if equipo.ubicacion:
                equipo.ubicacion = equipo.ubicacion.strip().capitalize()
            if equipo.estado:
                equipo.estado = equipo.estado.strip().capitalize()
            if equipo.tipo_equipo and equipo.tipo_equipo.lower() == 'pc':
                equipo.tipo_equipo = 'PC'

            # Guardar si hubo cambios
            nuevo = (equipo.tipo_equipo, equipo.ubicacion, equipo.estado)
            if nuevo != original:
                equipo.save()
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(f'{actualizados} registros actualizados correctamente.'))
