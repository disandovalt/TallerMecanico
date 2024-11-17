from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Página para seleccionar el rol (Administrador o Usuario)
def seleccion_rol(request):
    if request.method == 'POST':
        rol = request.POST.get('rol')
        if rol == 'admin':
            return redirect('login?rol=admin')
        elif rol == 'user':
            return redirect('login?rol=user')
    return render(request, 'core/seleccion_rol.html')

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
