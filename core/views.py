from django.shortcuts import  redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
