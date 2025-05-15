from django.core.management.base import BaseCommand
from inventario.models import Inventario

class Command(BaseCommand):
    help = 'Actualiza campos con formato correcto'

    def handle(self, *args, **kwargs):
        total = 0
        for equipo in Inventario.objects.all():
            actualizado = False

            if equipo.ubicacion:
                ubicacion = equipo.ubicacion.capitalize()
                if equipo.ubicacion != ubicacion:
                    equipo.ubicacion = ubicacion
                    actualizado = True

            if equipo.estado:
                estado = equipo.estado.capitalize()
                if equipo.estado != estado:
                    equipo.estado = estado
                    actualizado = True

            if equipo.tipo_equipo:
                tipo = equipo.tipo_equipo.upper()
                if equipo.tipo_equipo != tipo:
                    equipo.tipo_equipo = tipo
                    actualizado = True

            if actualizado:
                equipo.save()
                total += 1

        self.stdout.write(self.style.SUCCESS(f'{total} registros actualizados correctamente.'))
