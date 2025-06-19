from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
import uuid

User = get_user_model()

class Candidato(models.Model):
    nombre = models.CharField(max_length=100)
    partido = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='candidatos/')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre



class Sexo(models.Model):
    """Género"""
    MASCULINO = 'M'
    FEMENINO  = 'F'
    OPCIONES  = [
        (MASCULINO, 'Masculino'),
        (FEMENINO,  'Femenino'),
    ]

    id          = models.AutoField(primary_key=True)
    descripcion = models.CharField(
        max_length=1,
        choices=OPCIONES,
        default=MASCULINO,
        unique=True,
        verbose_name='Sexo'
    )

    class Meta:
        db_table = 'sexo'
        verbose_name = 'Sexo'
        verbose_name_plural = 'Sexos'

    def __str__(self):
        return self.get_descripcion_display()


class Ubicacion(models.Model):
    id     = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100, unique=True, verbose_name='Región')

    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.region



# Validador de RUT chileno SIN puntos, solo con guión y dígito verificador
rut_validator = RegexValidator(
    regex=r'^\d{7,8}-[\dkK]$',
    message='Formato de RUT inválido. Debe ingresarse SIN puntos y CON guión: 12345678-5'
)



class Usuario(models.Model):
    """Perfil de usuario con campos completos de registro."""
    REGION_CHOICES = [
        ('Arica y Parinacota', 'Arica y Parinacota'),
        ('Tarapacá', 'Tarapacá'),
        ('Antofagasta', 'Antofagasta'),
        ('Atacama', 'Atacama'),
        ('Coquimbo', 'Coquimbo'),
        ('Valparaíso', 'Valparaíso'),
        ('Metropolitana de Santiago', 'Metropolitana de Santiago'),
        ("O'Higgins", "O'Higgins"),
        ('Maule', 'Maule'),
        ('Ñuble', 'Ñuble'),
        ('Biobío', 'Biobío'),
        ('La Araucanía', 'La Araucanía'),
        ('Los Ríos', 'Los Ríos'),
        ('Los Lagos', 'Los Lagos'),
        ('Aysén', 'Aysén'),
        ('Magallanes', 'Magallanes'),
    ]

    #
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    rut = models.CharField(
        'RUT',
        max_length=10,           
        primary_key=True,
        validators=[rut_validator]
    )
    nombre      = models.CharField('Nombre completo', max_length=150)
    email       = models.EmailField('Mail', unique=True)
    contraseña  = models.CharField('Contraseña', max_length=128)
    edad        = models.PositiveIntegerField('Edad')
    region      = models.CharField(
                     'Región',
                     max_length=50,
                     choices=REGION_CHOICES,
                     default='Metropolitana de Santiago'
                  )
    sexo        = models.CharField(
                     'Sexo',
                     max_length=1,
                     choices=SEXO_CHOICES
                  )


    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.rut} — {self.nombre}"


class Candidato(models.Model):
    id      = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=150)
    partido = models.CharField(max_length=100)

    class Meta:
        db_table = 'candidato'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

    def __str__(self):
        return self.nombre


class Afinidad(models.Model):
    id         = models.AutoField(primary_key=True)
    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='rut_usuario')
    candidato  = models.ForeignKey(Candidato, on_delete=models.CASCADE, db_column='id_candidato')
    porcentaje = models.FloatField()

    class Meta:
        db_table = 'afinidad'
        verbose_name = 'Afinidad'
        verbose_name_plural = 'Afinidades'
        unique_together = ('usuario', 'candidato')


class Pregunta(models.Model):
    id     = models.AutoField(primary_key=True)
    texto  = models.TextField()
    orden  = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'pregunta'
        ordering = ['orden']
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return f"{self.orden}. {self.texto}"


class Alternativa(models.Model):
    id          = models.AutoField(primary_key=True)
    pregunta    = models.ForeignKey(Pregunta, on_delete=models.CASCADE, db_column='id_pregunta')
    texto       = models.TextField()
    valor       = models.IntegerField()

    class Meta:
        db_table = 'alternativa'
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'

    def __str__(self):
        return f"{self.pregunta.orden}-{self.valor}: {self.texto}"
    
class Ponderacion(models.Model):
    alternativa = models.ForeignKey(
        Alternativa,
        on_delete=models.CASCADE,
        related_name='ponderaciones'
    )
    candidato   = models.ForeignKey(
        Candidato,
        on_delete=models.CASCADE,
        related_name='ponderaciones'
    )
    peso         = models.FloatField()

    class Meta:
        db_table = 'ponderacion'
        verbose_name = 'Ponderación'
        verbose_name_plural = 'Ponderaciones'
        unique_together = ('alternativa', 'candidato')

    def __str__(self):
        return f"{self.alternativa} → {self.candidato}: {self.peso}"



class RespuestaUsuario(models.Model):
    id           = models.AutoField(primary_key=True)
    usuario      = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='rut_usuario')
    pregunta     = models.ForeignKey(Pregunta, on_delete=models.CASCADE, db_column='id_pregunta')
    alternativa  = models.ForeignKey(Alternativa, on_delete=models.CASCADE, db_column='id_alternativa')

    class Meta:
        db_table = 'respuesta_usuario'
        verbose_name = 'Respuesta de Usuario'
        verbose_name_plural = 'Respuestas de Usuario'
        unique_together = ('usuario', 'pregunta')


class Task(models.Model):
    title         = models.CharField(max_length=200)
    description   = models.TextField(blank=True)
    created       = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important     = models.BooleanField(default=False)
    user          = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.title} — by {self.user.username}"
