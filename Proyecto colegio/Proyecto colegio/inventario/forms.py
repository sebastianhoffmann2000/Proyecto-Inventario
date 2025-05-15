from django import forms
from .models import Inventario
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget

class InventarioForm(forms.ModelForm):
    fecha_inicio_prestamo = forms.DateField(
        widget=SelectDateWidget(years=range(2020, 2031)),
        required=False
    )
    fecha_fin_prestamo = forms.DateField(
        widget=SelectDateWidget(years=range(2020, 2031)),
        required=False
    )
    fecha_adquisicion = forms.DateField(
        widget=SelectDateWidget(years=range(2020, 2031)),
        required=False
    )

    class Meta:
        model = Inventario
        fields = [
            'equipo', 'tipo_equipo', 'marca', 'modelo',
            'ubicacion', 'estado', 'detalle', 'foto',
            'prestamo_activo', 'nombre_solicitante',
            'fecha_inicio_prestamo', 'fecha_fin_prestamo',
            'fondo_adquisicion', 'fecha_adquisicion'
        ]
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fondo_adquisicion': forms.Select(attrs={'class': 'form-select'}),
            'subvencion_escolar': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio_prestamo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin_prestamo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio_prestamo')
        fecha_fin = cleaned_data.get('fecha_fin_prestamo')
        if cleaned_data.get('fondo_adquisicion') == 'SEP' and not cleaned_data.get('subvencion_escolar'):
            raise ValidationError('Si el fondo es SEP, debe completar "Subvención escolar".')
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValidationError('La fecha de fin no puede ser antes de la fecha de inicio.')
        return cleaned_data
