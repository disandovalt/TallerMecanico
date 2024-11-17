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


some_date = datetime.now() - timedelta(days=7)
# Página para seleccionar el rol (Administrador o Usuario)
def seleccion_rol(request):
    if request.method == 'POST':
        rol = request.POST.get('rol')  # Obtiene el rol seleccionado desde el formulario
        
        # Redirige a la página de login pasando el rol como parte de la URL
        if rol == 'admin':
            return redirect('login_admin')
        elif rol == 'usuario':
            return redirect('login_usuario')
    
    return render(request, '../templates/core/seleccion_rol.html')


# Página de inicio de sesión
def login_view(request):
    rol = request.GET.get('rol', 'user')  # Obtiene el rol desde la URL (por defecto 'user')
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirigir según el rol
            if rol == 'admin':
                return redirect('/admin')  # Redirige al panel de administración
            else:
                return redirect('/')  # Redirige a la página principal

    return render(request, 'core/login.html', {'form': form, 'rol': rol})


def inicio(request):
    return render(request, 'inicio.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Verificar si es admin
            login(request, user)
            return HttpResponseRedirect('/admin_dashboard/')  # Redirigir al dashboard de admin
        else:
            return render(request, 'core/login_admin.html', {'error': 'Credenciales incorrectas o no es administrador'})
    
    return render(request, 'core/login_admin.html')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:  # Verificar que no sea admin
            login(request, user)
            return HttpResponseRedirect('/user_dashboard/')  # Redirigir al dashboard de usuario
        else:
            return render(request, 'core/login_usuario.html', {'error': 'Credenciales incorrectas o no es un usuario'})
    
    return render(request, 'core/login_usuario.html')

def dashboard(request):
    # Datos de ejemplo para mostrar en la página
    total_usuarios = User.objects.count()
    total_ordenes = OrdenTrabajo.objects.count()
    total_inventario = Inventario.objects.count()
    total_clientes = Cliente.objects.count()  # Agregar el total de clientes

    ordenes = OrdenTrabajo.objects.filter(fecha__gte=some_date)
    
    return render(request, 'core/admin_dashboards.html', {
        'total_usuarios': total_usuarios,
        'total_ordenes': total_ordenes,
        'total_inventario': total_inventario,
        'total_clientes': total_clientes,
        'ordenes': ordenes,
    })

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

# Vista para editar una orden de trabajo existente
def editar_orden(request, orden_id):
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('listar_ordenes')
    else:
        form = OrdenTrabajoForm(instance=orden)
    return render(request, 'core/editar_orden.html', {'form': form})

# Vista para eliminar una orden de trabajo
def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenTrabajo, id=orden_id)
    if request.method == 'POST':
        orden.delete()
        return redirect('listar_ordenes')
    return render(request, 'core/eliminar_orden.html', {'orden': orden})




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


def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/listar_clientes.html', {'clientes': clientes})

class ListarClientesView(ListView):
    model = Cliente
    template_name = 'core/listar_clientes.html'
    context_object_name = 'clientes'

    
class CrearClienteView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'core/crear_cliente.html'
    success_url = reverse_lazy('listar_clientes')


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Aquí se guarda el cliente en la base de datos
            return redirect('core/listar_clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm()

    return render(request, 'core/crear_cliente.html', {'form': form})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list') 
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/editar_cliente.html', {'form': form, 'cliente': cliente})

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