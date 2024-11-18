from django import forms
from django.contrib.auth.models import User, Group
from .models import OrdenTrabajo, Inventario, Cliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from core.models import Producto

class CustomUserCreationForm(UserCreationForm):
    ROLES = [
        ('Mecánico', 'Mecánico'),
        ('Recepcionista', 'Recepcionista'),
    ]
    
    rol = forms.ChoiceField(
        choices=ROLES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Asignar el rol seleccionado
            role = self.cleaned_data['rol']
            group = Group.objects.get(name=role)
            user.groups.add(group)
        return user
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class UserForm(UserCreationForm):
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = User  # Usamos el modelo User estándar de Django
        fields = ['username', 'email', 'telefono', 'is_staff', 'is_superuser']  # Incluye los campos que deseas

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

class ClienteForm(forms.ModelForm):
    class Meta:
        
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email', 'direccion'] 
        

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['cliente', 'descripcion', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un cliente'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa el trabajo a realizar'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            })
        }

# Formulario para crear un cliente
    
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'cantidad', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
from .models import Usuario  
class UsuarioCreateForm(UserCreationForm):
    # Opciones de rol
    ROL_CHOICES = [
        ('mecanico', 'Mecánico'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    rol = forms.ChoiceField(choices=ROL_CHOICES, required=True, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']

class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario  # Asegúrate de usar el modelo Usuario aquí
        fields = ['email', 'nombre', 'telefono', 'direccion', 'rol', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UsuarioCreationForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'telefono', 'direccion', 'rol', 'is_active']

    # Puedes agregar validaciones personalizadas si es necesario
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email
    
class CustomUserCreationForm(UserCreationForm):
    pass
    
class UsuarioForm(UserCreationForm):
    # Aquí puedes agregar los campos adicionales de tu usuario
    class Meta:
        model = get_user_model()
        fields = ['email', 'nombre', 'telefono', 'direccion', 'rol', 'is_active']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'precio']

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['cliente', 'descripcion', 'estado']  # Ajusta los campos según lo necesario
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

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
    

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from core.models import Cliente
from django.core.exceptions import ValidationError
    
def registro_cliente(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.POST.get('correo')
        password = request.POST.get('contrasena')
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        apellido = request.POST.get('apellido')

        # Verificar si el correo no está vacío
        if not email:
            return render(request, 'registro_cliente.html', {'error': 'El correo es obligatorio'})

        # Verificar si el email es válido
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'registro_cliente.html', {'error': 'Correo electrónico inválido'})

        # Verificar si las contraseñas coinciden
        if password != request.POST.get('confirmar_contrasena'):
            return render(request, 'registro_cliente.html', {'error': 'Las contraseñas no coinciden'})

        # Crear el usuario
        try:
            user = get_user_model().objects.create_user(email=email, password=password, nombre=nombre)
            user.save()
        except Exception as e:
            return render(request, 'registro_cliente.html', {'error': f'Error al crear el usuario: {e}'})

        # Crear el cliente asociado al usuario
        try:
            cliente = Cliente.objects.create(
                usuario=user,
                rut=rut,
                telefono=telefono,
                direccion=direccion,
                email=email,
                nombre=nombre,
                apellido=apellido
            )
            cliente.save()  # Guardar el cliente en la base de datos
        except Exception as e:
            return render(request, 'registro_cliente.html', {'error': f'Error al crear el cliente: {e}'})

        # Redirigir al login o mostrar un mensaje de éxito
        return redirect('login_cliente')

    # Si no es un POST, mostrar el formulario
    return render(request, 'registro_cliente.html')

from datetime import datetime, timedelta
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'descripcion_servicio', 'marca_vehiculo', 'modelo_vehiculo', 'ano_vehiculo']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': datetime.now().date().isoformat()
                }
            ),
            'hora': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'descripcion_servicio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
            'marca_vehiculo': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'modelo_vehiculo': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'ano_vehiculo': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha:
            # Verifica que la fecha no sea en el pasado
            if fecha < datetime.now().date():
                raise forms.ValidationError("No puedes hacer reservas en fechas pasadas")

            # Verifica que la fecha sea un día laboral (Lunes a Sábado)
            if fecha.weekday() == 6:  # Domingo
                raise forms.ValidationError("No se pueden hacer reservas los domingos")

            # Verifica si ya existe una reserva para esa fecha y hora
            if hora and Reserva.objects.filter(fecha=fecha, hora=hora).exists():
                raise forms.ValidationError("Esta hora ya está reservada. Por favor elige otro horario.")

        return cleaned_data