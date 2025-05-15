from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('listar/', views.listar_inventario, name='listar_inventario'),
    path('registrar/', views.registrar_equipo, name='registrar_equipo'),
    path('detalle/<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),  # corregido
    path('editar/<int:equipo_id>/', views.editar_equipo, name='editar_equipo'),     # ya estaba bien
    path('inventario/eliminar/<int:equipo_id>/', views.eliminar_equipo, name='eliminar_equipo'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('buscar/', views.buscar_inventario, name='buscar_inventario'),
    path('escanear/', views.escanear_codigo, name='escanear_codigo'),
    path('actualizar_prestamo/<int:equipo_id>/', views.actualizar_prestamo, name='actualizar_prestamo'),  # corregido
    path('', views.inventario, name='inventario'),
     path('inicio/', views.index, name='index'),
    path('generar_codigo_barra/', views.generar_codigo_barra, name='generar_codigo_barra'),
]
