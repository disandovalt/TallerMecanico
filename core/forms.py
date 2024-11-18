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