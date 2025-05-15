from django.core.management.base import BaseCommand
from inventario.models import Inventario

class Command(BaseCommand):
    help = 'Actualiza ubicación y estado con inicial en mayúscula y tipo_equipo en mayúsculas completas.'

    def handle(self, *args, **kwargs):
        total = 0
        for equipo in Inventario.objects.all():
            actualizado = False

            if equipo.ubicacion:
                nueva_ubicacion = equipo.ubicacion.capitalize()
                if equipo.ubicacion != nueva_ubicacion:
                    equipo.ubicacion = nueva_ubicacion
                    actualizado = True

            if equipo.estado:
                nuevo_estado = equipo.estado.capitalize()
                if equipo.estado != nuevo_estado:
                    equipo.estado = nuevo_estado
                    actualizado = True

            if equipo.tipo_equipo:
                nuevo_tipo = equipo.tipo_equipo.upper()
                if equipo.tipo_equipo != nuevo_tipo:
                    equipo.tipo_equipo = nuevo_tipo
                    actualizado = True

            if actualizado:
                equipo.save()
                total += 1

        self.stdout.write(self.style.SUCCESS(f'{total} registros actualizados correctamente.'))
