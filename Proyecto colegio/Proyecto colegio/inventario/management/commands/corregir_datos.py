from django.core.management.base import BaseCommand
from inventario.models import Inventario

class Command(BaseCommand):
    help = 'Corrige las ubicaciones, estados y tipo_equipo para que coincidan con los choices'

    def handle(self, *args, **kwargs):
        ubicaciones_validas = [k for k, _ in Inventario.UBICACION_CHOICES]
        estados_validos = [k for k, _ in Inventario.ESTADO_CHOICES]
        total_actualizados = 0

        for equipo in Inventario.objects.all():
            cambiado = False

            for k in ubicaciones_validas:
                if equipo.ubicacion and equipo.ubicacion.lower() == k.lower() and equipo.ubicacion != k:
                    equipo.ubicacion = k
                    cambiado = True

            for k in estados_validos:
                if equipo.estado and equipo.estado.lower() == k.lower() and equipo.estado != k:
                    equipo.estado = k
                    cambiado = True

            if equipo.tipo_equipo and equipo.tipo_equipo.lower() == 'pc' and equipo.tipo_equipo != 'PC':
                equipo.tipo_equipo = 'PC'
                cambiado = True

            if cambiado:
                equipo.save()
                total_actualizados += 1

        self.stdout.write(self.style.SUCCESS(f'{total_actualizados} registros fueron corregidos.'))
