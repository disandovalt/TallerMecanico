from django.shortcuts import  redirect,  get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Inventario, OrdenTrabajo
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .forms import OrdenTrabajoForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import OrdenTrabajoForm
from .models import Cliente
from .forms import ClienteForm
from datetime import timedelta, datetime
from .forms import CustomUserForm
from .forms import CustomUserCreationForm
from django.views import View
from django.utils import timezone
from datetime import datetime
from django.utils.formats import date_format
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required, user_passes_test
from .permissions import setup_roles_and_permissions, role_required
from django.db.models import Count
from .forms import UsuarioEditForm
from django.contrib.auth import get_user_model
from core.forms import CustomUserCreationForm
from .models import Producto


User = get_user_model()
usuarios = User.objects.all()


some_date = datetime.now() - timedelta(days=7)
# Página para seleccionar el rol (Administrador o Usuario)
def seleccion_rol(request):
    if request.method == 'POST':
        rol = request.POST.get('rol')  # Obtiene el rol seleccionado desde el formulario
        
        # Redirige a la página de login pasando el rol como parte de la URL
        if rol == 'admin':
            return redirect('login_admin')
        elif rol == 'usuario':
            return redirect('login_cliente')
    
    return render(request, '../templates/core/seleccion_rol.html')


# Página de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si las credenciales son correctas, loguear al usuario
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('seleccion_rol')  # O la URL a donde redirigir al usuario
        else:
            # Si las credenciales son incorrectas
            messages.error(request, "Credenciales incorrectas.")
    
    # Si no es un POST, simplemente renderiza el formulario de login
    return render(request, 'core/base.html')

def redirect_by_role(user):
    if user.rol == 'administrador':
        return redirect('admin_dashboards')
    elif user.rol == 'mecanico':
        return redirect('mecanico_dashboard')
    elif user.rol == 'recepcionista':
        return redirect('recepcionista_dashboard')
    elif user.rol == 'usuario':
        try:
            cliente = Cliente.objects.get(email=user.email)
            return redirect('usuario_dashboard')
        except Cliente.DoesNotExist:
            messages.warning(user, 'No tiene un perfil de cliente asociado')
            return redirect('login')
    return redirect('login')

def es_mecanico(user):
    return user.rol == 'mecanico'

def es_recepcionista(user):
    return user.rol == 'recepcionista'

def es_administrador(user):
    return user.rol == 'administrador'

@login_required
@user_passes_test(es_mecanico)
def mecanico_dashboard(request):
    ordenes = OrdenTrabajo.objects.filter(estado='Pendiente')
    inventario = Inventario.objects.all()
    return render(request, 'mecanico/dashboard.html', {
        'ordenes': ordenes,
        'inventario': inventario
    })

@login_required
@user_passes_test(es_recepcionista)
def recepcionista_dashboard(request):
    clientes = Cliente.objects.all()
    ordenes = OrdenTrabajo.objects.all()
    return render(request, 'recepcionista/dashboard.html', {
        'clientes': clientes,
        'ordenes': ordenes
    })

@login_required
@user_passes_test(es_administrador)
def admin_dashboard(request):
    usuarios = Usuario.objects.all()
    productos = Producto.objects.all()
    return render(request, 'admin/dashboard.html', {
        'usuarios': usuarios,
        'productos': productos
    })

@login_required
def usuario_dashboard(request):
    try:
        # Intentar obtener el cliente asociado al usuario
        cliente = Cliente.objects.get(email=request.user.email)
        ordenes = OrdenTrabajo.objects.filter(cliente=cliente)
        
        return render(request, 'usuario/dashboard.html', {
            'ordenes': ordenes,
            'cliente': cliente
        })
    except Cliente.DoesNotExist:
        messages.error(request, 'No se encontró un cliente asociado a este usuario')
        return redirect('login')


def inicio(request):
    return render(request, 'inicio.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Verificar si es admin
            login(request, user)
            return HttpResponseRedirect('/admin_dashboards/')  # Redirigir al dashboard de admin
        else:
            return render(request, 'core/login_admin.html', {'error': 'Credenciales incorrectas o no es administrador'})
    
    return render(request, 'core/login_admin.html')

def login_cliente(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # O la página a la que deseas redirigir
        else:
            return render(request, 'core\login_cliente.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'core\login_cliente.html')

from core.forms import RegistroClienteForm

def registrar_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('') 
    else:
        form = ClienteForm()

    return render(request, 'core/registrar_cliente.html', {'form': form})

@login_required
def dashboard(request):
    # Obtener la fecha actual
    hoy = timezone.now()
    hace_30_dias = hoy - timedelta(days=30)

    # Estadísticas generales
    context = {
        'total_usuarios': User.objects.count(),
        'total_ordenes': OrdenTrabajo.objects.count(),
        'total_inventario': Inventario.objects.count(),
        'total_clientes': Cliente.objects.count(),
        
        # Órdenes recientes
        'ordenes_recientes': OrdenTrabajo.objects.select_related('cliente').order_by('-fecha')[:10],
        
        # Estadísticas de estados de órdenes
        'estados_ordenes': OrdenTrabajo.objects.values('estado').annotate(
            total=Count('id')
        ),
        
        # Órdenes por día (últimos 30 días)
        'ordenes_por_dia': OrdenTrabajo.objects.filter(
            fecha__gte=hace_30_dias
        ).values('fecha__date').annotate(
            total=Count('id')
        ).order_by('fecha__date'),
    }
    
    return render(request, 'core/admin_dashboards.html', context)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir o mostrar un mensaje
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def listar_usuarios(request):
    # Obtener todos los usuarios
    usuarios = User.objects.all()
    
    # Pasar los usuarios a la plantilla
    return render(request, 'core/listar_usuarios.html', {'usuarios': usuarios})


# Vista para crear un nuevo usuario
from django.shortcuts import render, redirect
from .forms import CustomUserForm

def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')  # Cambia según tu flujo
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/crear_usuario.html', {'form': form})


# Vista para editar un usuario existente
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')  # Redirige a la lista de usuarios
    else:
        form = UserChangeForm(instance=usuario)
    return render(request, 'core/editar_usuario.html', {'form': form, 'usuario': usuario})

# Vista para eliminar un usuario
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    return redirect('listar_usuarios')  # Redirige a la lista de usuarios






def listar_ordenes(request):
    ordenes = OrdenTrabajo.objects.all()
    return render(request, 'core/listar_ordenes.html', {'ordenes': ordenes})

def crear_orden_trabajo(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orden de trabajo creada exitosamente.')
            return redirect('listar_ordenes')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = OrdenTrabajoForm()
    
    return render(request, 'core/crear_orden.html', {
        'form': form,
        'titulo': 'Crear Nueva Orden de Trabajo'
    })
from core.models import OrdenTrabajo
from core.forms import OrdenTrabajoForm
# Vista para editar una orden de trabajo existente
def editar_orden_trabajo(request, orden_id):
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('listar_ordenes')  # Ajusta el nombre de esta URL según tu proyecto
    else:
        form = OrdenTrabajoForm(instance=orden)

    return render(request, 'core/editar_orden.html', {'form': form, 'orden': orden})

def listar_inventarios(request):
    inventarios = Inventario.objects.all()
    return render(request, 'core/listar_inventarios.html', {'inventarios': inventarios})

# Vista para crear un nuevo inventario
def crear_inventario(request):
    if request.method == 'POST':
        # Aquí puedes agregar tu formulario para crear un inventario
        pass
    return render(request, 'core/crear_inventario.html')

# Vista para editar un inventario existente
def editar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST':
        # Lógica para editar el inventario
        pass
    return render(request, 'core/editar_inventario.html', {'inventario': inventario})

# Vista para eliminar un inventario
def eliminar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    inventario.delete()
    return redirect('core/listar_inventarios.html')


class ListarClientesView(ListView):
    model = Cliente
    template_name = 'core/listar_clientes.html'
    context_object_name = 'clientes'

    
class CrearClienteView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'core/crear_cliente.html'
    success_url = reverse_lazy('listar_clientes')

class EditarClienteView(View):
    def get(self, request, rut):
        cliente = get_object_or_404(Cliente, rut=rut)
        return render(request, 'editar_cliente.html', {'cliente': cliente})

    def post(self, request, rut):
        # Lógica para guardar cambios
        pass


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Aquí se guarda el cliente en la base de datos
            return redirect('core/listar_clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm()

    return render(request, 'core/crear_cliente.html', {'form': form})

def editar_cliente(request, rut):
    cliente = get_object_or_404(Cliente, rut=rut)

    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.telefono = request.POST['telefono']
        cliente.email = request.POST['email']
        cliente.direccion = request.POST['direccion']
        cliente.save()
        # Corregimos la redirección para usar el nombre de la URL
        return redirect('listar_clientes')  # Este debe coincidir con el name en urls.py

    return render(request, 'core/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, rut):
    cliente = get_object_or_404(Cliente, rut=rut)  # Obtener el cliente por su rut
    cliente.delete()  # Eliminar el cliente
    return redirect('listar_clientes')

def listar_ordenes(request):
    # Obtener el RUT del parámetro GET
    rut_filter = request.GET.get('rut', '')
    
    # Filtrar las órdenes
    if rut_filter:
        ordenes = OrdenTrabajo.objects.filter(cliente__rut__icontains=rut_filter).order_by('-fecha')
    else:
        ordenes = OrdenTrabajo.objects.all().order_by('-fecha')
    
    return render(request, 'core/listar_ordenes.html', {
        'ordenes': ordenes,
    })

@permission_required('app.add_ordentrabajo')
def vista_restringida(request):
    # Lógica de la vista
    return render(request, 'some_template.html')


@login_required
@role_required(['Administrador'])
def configurar_roles(request):
    setup_roles_and_permissions()
    messages.success(request, 'Roles y permisos configurados exitosamente')
    return redirect('admin:index')

@login_required
@role_required(['Mecánico'])
def vista_mecanico(request):
    # Solo accesible por mecánicos
    pass

@login_required
@role_required(['Recepcionista'])
def vista_recepcionista(request):
    # Solo accesible por recepcionistas
    pass

@login_required
@role_required(['Mecánico', 'Recepcionista'])
def vista_compartida(request):
    # Accesible por ambos roles
    pass


def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')  # Ajusta la URL según tu aplicación
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'core/editar_usuario.html', {'form': form})


from django import forms
from core.models import Usuario

from django.contrib.auth.models import Group
from core.forms import UsuarioEditForm

from core.forms import UsuarioForm

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        
        # Validación de contraseñas
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            form.add_error('confirm_password', 'Las contraseñas no coinciden')

        if form.is_valid():
            # Crear el usuario pero no lo guardes todavía
            usuario = form.save(commit=False)
            
            # Encriptar la contraseña
            usuario.set_password(password)
            
            # Asegurarte de que el rol esté en minúsculas antes de asignarlo
            rol = form.cleaned_data['rol'].lower()
            if rol not in ['mecanico', 'recepcionista', 'usuario', 'administrador']:
                form.add_error('rol', 'Rol no válido')
            else:
                # Asignar el grupo basado en el valor del rol
                group = Group.objects.get(name=rol.capitalize())
                usuario.groups.add(group)
                
                # Guardar el usuario
                usuario.save()

            return redirect('listar_usuarios')  # Redirige a la lista de usuarios
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

@login_required
@role_required(['Administrador'])  # Solo administradores pueden crear usuarios
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario con los datos del formulario
            messages.success(request, f'Usuario {user.email} creado exitosamente')  # Usar 'email' en lugar de 'username'
            return redirect('listar_usuarios')  # Redirige a la lista de usuarios
    else:
        form = CustomUserCreationForm()  # Si es un GET, solo muestra el formulario vacío

    return render(request, 'core/crear_usuario.html', {'form': form})

from .forms import ProductoForm


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el producto en la base de datos
            return redirect('listar_inventarios')  # Redirige a la lista de inventarios
    else:
        form = ProductoForm()

    return render(request, 'core/crear_inventario.html', {'form': form})

def listar_inventarios(request):
    productos = Producto.objects.all()
    return render(request, 'core/listar_inventarios.html', {'productos': productos})


def eliminar_orden_trabajo(request, orden_id):
    orden = get_object_or_404(Cliente, id=orden_id)
    orden.delete()
    return redirect(reverse('core/admin_dashboards'))  # Ajusta esta URL según tu proyecto

def filtrar_clientes(request):
    rut_filter = request.GET.get('rut', '')  # Obtiene el valor del filtro del formulario

    # Filtrar los clientes
    if rut_filter:
        clientes = Cliente.objects.filter(rut__icontains=rut_filter)  # Filtra por coincidencia parcial del RUT
    else:
        clientes = Cliente.objects.all()  # Muestra todos los clientes si no hay filtro

    return render(request, 'core/listar_clientes.html', {
        'clientes': clientes,  # Asegúrate de usar 'clientes' en el contexto
    })

class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email', 'direccion', 'contraseña']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if password != confirmar_contrasena:
            raise forms.ValidationError('Las contraseñas no coinciden')

        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        user = User.objects.create_user(username=cliente.email, email=cliente.email, password=self.cleaned_data['password'])
        cliente.usuario = user  # Relacionamos el cliente con el usuario creado
        if commit:
            cliente.save()
        return cliente
    
from .forms import ReservaForm
from .models import Reserva
    
@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            # Verificar si el usuario tiene un cliente asociado
            try:
                reserva.cliente = request.user.cliente
            except AttributeError:
                messages.error(request, 'El usuario no tiene un cliente asociado.')
                return redirect('perfil_cliente')  # Redirigir al perfil de cliente (ajusta la vista como sea necesario)

            reserva.save()
            messages.success(request, '¡Reserva creada exitosamente!')
            return redirect('ver_reservas')
    else:
        form = ReservaForm()

    return render(request, 'core/reserva.html', {'form': form})

@login_required
def ver_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user.cliente)
    return render(request, 'core/ver_reservas.html', {'reservas': reservas})