from django import forms
from django.contrib.auth.models import User
from .models import OrdenTrabajo,  Usuario, Inventario, Cliente
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']  # Los campos que queremos en el formulario
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
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

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'direccion', 'is_staff']  # Campos del modelo Usuario

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data

    def save(self, commit=True):
        # Guardar el usuario pero con la contraseña cifrada
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Establecer la contraseña cifrada
        if commit:
            user.save()  # Guardar en la base de datos
        return user
    
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

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    direccion = forms.CharField(required=True)
    rol = forms.ChoiceField(choices=[('admin', 'Admin'), ('usuario', 'Usuario')], required=True)

    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'telefono', 'direccion', 'rol', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nombre = self.cleaned_data['nombre']
        user.telefono = self.cleaned_data['telefono']
        user.direccion = self.cleaned_data['direccion']
        user.rol = self.cleaned_data['rol']
        
        if commit:
            user.save()
        return user