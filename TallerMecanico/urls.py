"""
URL configuration for TallerMecanico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from core.views import ListarClientesView
from core.views import CrearClienteView
from core.views import crear_orden_trabajo
from core.views import EditarClienteView
from core.views import editar_cliente, listar_clientes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.seleccion_rol, name='seleccion_rol'),
    path('login/', views.login_view, name='login'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('login/usuario/', views.login_usuario, name='login_usuario'),
    path('admin_dashboards/', views.dashboard, name='admin_dashboards'),

    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # URLs para CRUD de Órdenes de Trabajo
    path('ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('ordenes/crear/', views.crear_orden_trabajo, name='crear_orden_trabajo'),
    path('ordenes/editar/<int:orden_id>/', views.editar_orden_trabajo, name='editar_orden'),
    path('ordenes/eliminar/<int:orden_id>/', views.eliminar_orden_trabajo, name='eliminar_orden'),

    # URLs para CRUD de Inventario
    path('listar_inventarios/', views.listar_inventarios, name='listar_inventarios'),
    path('crear_inventario/', views.crear_inventario, name='crear_inventario'),
    path('editar_inventario/<int:inventario_id>/', views.editar_inventario, name='editar_inventario'),
    path('eliminar_inventario/<int:inventario_id>/', views.eliminar_inventario, name='eliminar_inventario'),

    path('clientes/', views.ListarClientesView.as_view(), name='listar_clientes'),
    path('clientes/', ListarClientesView.as_view(), name='listar_clientes'),
    path('clientes/crear/', CrearClienteView.as_view(), name='crear_cliente'),
    path('clientes/eliminar/<str:rut>/', views.eliminar_cliente, name='eliminar_cliente'),

    path('clientes/editar/<str:rut>/', editar_cliente, name='editar_cliente'),
    path('clientes/', listar_clientes, name='listar_clientes'), 

]
