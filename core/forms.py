from django import forms
from django.contrib.auth.models import User
from .models import OrdenTrabajo, Inventario, Cliente
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 
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