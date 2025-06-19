from django.forms import ModelForm
from .models import Task
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import Usuario, Ubicacion, Sexo, Pregunta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# forms.py

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(
        label="Nuevo correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'El correo es obligatorio.',
            'invalid': 'Introduce un correo válido.'
        }
    )
    current_password = forms.CharField(
        label="Contraseña actual",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Debes ingresar tu contraseña actual.'}
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        pwd = self.cleaned_data.get("current_password")
        if not self.user.check_password(pwd):
            raise forms.ValidationError("La contraseña no coincide.")
        return pwd

    def clean_new_email(self):
        email = self.cleaned_data.get("new_email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ese correo ya está en uso.")
        return email

    

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        help_text="Mínimo 8 caracteres."
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

# Validador de RUT chileno (formato con o sin puntos, con guión y dígito verificador)
rut_validator = RegexValidator(
    regex=r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$',
    message='Formato de RUT inválido. Ej: 12.345.678-5 o 12345678-5'
)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'edad', 'region', 'sexo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
        }

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres',
        }),
        min_length=8,
        help_text='Mínimo 8 caracteres',
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 8 caracteres.'
        }
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
        }),
        error_messages={
            'required': 'Debes confirmar la contraseña.'
        }
    )

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'email', 'region', 'edad', 'sexo']
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-5',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'usuario@dominio.com',
            }),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 30',
                'min': 13,
            }),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'rut': {
                'required': 'El RUT es obligatorio.',
                'invalid': 'Formato de RUT inválido. Debe ser 12345678-5',
            },
            'nombre': {
                'required': 'El nombre completo es obligatorio.',
            },
            'email': {
                'required': 'El correo es obligatorio.',
                'invalid': 'El formato del correo no es válido.',
            },
            'edad': {
                'required': 'La edad es obligatoria.',
                'invalid': 'Debes ingresar un número válido (>=13).',
            },
            'region': {
                'required': 'Debes seleccionar una región.',
            },
            'sexo': {
                'required': 'Debes seleccionar tu sexo.',
            }
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '').strip()
        # 1) formato correcto
        rut_validator(rut)
        # 2) unicidad contra la tabla auth_user
        if User.objects.filter(username__iexact=rut).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese RUT.")
        return rut
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="RUT",
        max_length=10,
        validators=[rut_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-5',
            'id': 'id_username'
        }),
        error_messages={
            'required': 'Debes ingresar tu RUT.',
            'invalid': 'Formato de RUT inválido. Ej: 12345678-5'
        }
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu contraseña',
        }),
        error_messages={
            'required': 'Debes ingresar una contraseña.',
            'invalid': 'Contraseña incorrecta.'
        }
    )

    error_messages = {
        'invalid_login': 'RUT o contraseña incorrectos.',
        'inactive': 'Esta cuenta está inactiva.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para cada campo, si hay error, agregamos 'is-invalid'
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            if self.errors.get(name):
                field.widget.attrs['class'] = f"{css} is-invalid"


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['orden', 'texto']
        widgets = {
            'orden': forms.NumberInput(attrs={'class':'form-control'}),
            'texto': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }
        error_messages = {
            'orden': {'required': 'El orden es obligatorio.'},
            'texto': {'required': 'El texto es obligatorio.'},
        }