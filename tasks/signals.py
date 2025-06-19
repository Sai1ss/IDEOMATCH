from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Usuario          # tu modelo perfil (rut = username)

@receiver(post_delete, sender=User)
def borrar_perfil_usuario(sender, instance, **kwargs):
    """
    Cuando se elimina un registro de auth_user también
    borramos su perfil Usuario (la clave primaria es el RUT,
    que almacenamos en User.username). Las tablas que cuelgan
    de Usuario —Afinidad, RespuestaUsuario, etc.— ya usan
    on_delete=models.CASCADE, por lo que desaparecerán solas.
    """
    Usuario.objects.filter(rut=instance.username).delete()
