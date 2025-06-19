from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib import messages
from django.db import IntegrityError
from .forms import TaskForm, SignUpForm, CustomAuthenticationForm, PerfilForm, CustomPasswordChangeForm, Pregunta
from .models import Task, Usuario, Pregunta, Alternativa
from django.utils import timezone
import re
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import random

from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse


from django.db import transaction
from .models import Pregunta, Alternativa, RespuestaUsuario, Ponderacion, Afinidad, Usuario, Candidato
import pandas as pd

#imports de changepassword
from django.core.mail      import send_mail
from .forms                import EmailChangeForm
from .tokens               import email_change_token
#

from django.contrib.auth   import login, logout, authenticate, update_session_auth_hash, get_user_model
from django.contrib        import messages
#
import numpy as np
import plotly.express as px
from django.utils.safestring import mark_safe
from django.db.models import (
    F,
    Count,
    Avg,
    Window,
    ExpressionWrapper,
    IntegerField,
    Value)
from django.db.models.functions import RowNumber, Floor
import plotly.graph_objects as go
import json
from django.db.models import Func


# Sólo admins pueden acceder
def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff, login_url='home')(view))

@staff_required
def pregunta_list(request):
    preguntas = Pregunta.objects.order_by('orden')
    return render(request, 'preguntas.html', {
        'action': 'list',
        'preguntas': preguntas
    })

@staff_required
def pregunta_create(request):
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pregunta creada correctamente.")
            return redirect('pregunta_list')
    else:
        form = PreguntaForm()
    return render(request, 'preguntas.html', {
        'action': 'create',
        'preguntas': Pregunta.objects.order_by('orden'),
        'form': form
    })

@staff_required
def pregunta_update(request, pk):
    pregunta = get_object_or_404(Pregunta, pk=pk)
    if request.method == 'POST':
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            messages.success(request, "Pregunta actualizada correctamente.")
            return redirect('pregunta_list')
    else:
        form = PreguntaForm(instance=pregunta)
    return render(request, 'preguntas.html', {
        'action': 'update',
        'preguntas': Pregunta.objects.order_by('orden'),
        'form': form
    })

@staff_required
def pregunta_delete(request, pk):
    pregunta = get_object_or_404(Pregunta, pk=pk)
    if request.method == 'POST':
        pregunta.delete()
        messages.success(request, "Pregunta eliminada correctamente.")
        return redirect('pregunta_list')
    return render(request, 'preguntas.html', {
        'action': 'delete',
        'preguntas': Pregunta.objects.order_by('orden'),
        'pregunta': pregunta
    })

#-------------demas funciones del proyecto.-..............

class Floor(Func):
    function = 'FLOOR'
    arity = 1


User = get_user_model() 

RUT_REGEX = re.compile(r'^[0-9]{7,8}-[0-9Kk]$')

def signin(request):
   
    form = CustomAuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        # 1) Check formato RUT
        rut = request.POST.get('username', '').strip()
        if not rut:
            form.add_error('username', 'Debes ingresar un RUT valido.')
        elif not RUT_REGEX.match(rut):
            form.add_error('username', 'Formato de RUT inválido. Debe ser 12345678-5')

        # Si ya hay error de formato o vacío, lo mostramos y salimos
        if form.errors.get('username'):
            return render(request, 'signin.html', {'form': form})

        # 2) Existe usuario?
        if not User.objects.filter(username=rut).exists():
            form.add_error('username', 'No existe ninguna cuenta con ese RUT.')
            return render(request, 'signin.html', {'form': form})

        # 3) Autenticación de contraseña
        password = request.POST.get('password', '')
        if not password:
            form.add_error('password', 'Debes ingresar una contraseña.')
            return render(request, 'signin.html', {'form': form})

        user = authenticate(request, username=rut, password=password)
        if user is None:
            form.add_error('password', 'La contraseña no coincide con este RUT.')
            return render(request, 'signin.html', {'form': form})

        # 4) ¡Login exitoso!
        login(request, user)
        return redirect('home')

    return render(request, 'signin.html', {'form': form})



def como_funciona(request):
    return render(request, 'como_funciona.html')

def candidatos(request):
    return render(request, 'candidatos.html')


def lista_candidatos(request):
    candidatos = Candidato.objects.all()
    return render(request, 'candidatos.html', {'candidatos': candidatos})

def detalle_candidato(request, slug):
    candidato = get_object_or_404(Candidato, slug=slug)
    return render(request, 'candidato_detalle.html', {'candidato': candidato})

@login_required
def dashboard(request):
    # ① Afinidad top única por usuario ────────────────
    top_qs = (
        Afinidad.objects
        .annotate(
            rn=Window(
                expression=RowNumber(),
                partition_by=[F('usuario_id')],
                order_by=F('porcentaje').desc()
            )
        )
        .filter(rn=1)
        .select_related('usuario', 'candidato')
    )

    # ② Total de usuarios con al menos 1 respuesta
    total_users = (
        RespuestaUsuario.objects
        .values('usuario_id')
        .distinct()
        .count()
    )

    # ③ Helper para barras/tortas por candidato
    def agg_counts(qs):
        bar = (
            qs.values('candidato__nombre')
              .annotate(value=Count('usuario_id', distinct=True))
              .order_by('-value')
        )
        pie = (
            qs.values('candidato__nombre')
              .annotate(value=Avg('porcentaje'))
              .order_by('-value')
        )
        bar_list = [
            {'label': r['candidato__nombre'], 'value': r['value']}
            for r in bar
        ]
        pie_list = [
            {'label': r['candidato__nombre'], 'value': round(r['value'], 1)}
            for r in pie
        ]
        return bar_list, pie_list

    # ─────────────── GENERAL (por candidato) ────────────────
    bar_general, pie_general = agg_counts(top_qs)

    # ─────────────── BARRA POR SEXO (H / M) ────────────────
    sexo_qs = (
        top_qs
        .values('usuario__sexo')           # 'M' / 'F'
        .annotate(value=Count('usuario_id', distinct=True))
        .order_by('usuario__sexo')
    )
    bar_sexo = [
        {
            'label': 'Hombres' if r['usuario__sexo'] == 'M' else 'Mujeres',
            'value': r['value']
        }
        for r in sexo_qs
    ]

    # ─────────────── BARRA POR REGIÓN ───────────────────────
    region_qs = (
        top_qs
        .exclude(usuario__region='')
        .values('usuario__region')
        .annotate(value=Count('usuario_id', distinct=True))
        .order_by('usuario__region')
    )
    bar_region = [
        {'label': r['usuario__region'], 'value': r['value']}
        for r in region_qs
    ]

    # ─────────────── BARRA POR RANGO ETARIO ────────────────
    age_qs = (
        top_qs
        .filter(usuario__edad__gte=18)
        .annotate(
            rango=ExpressionWrapper(
                Floor(F('usuario__edad') / Value(10.0)) * Value(10),
                output_field=IntegerField()
            )
        )
        .values('rango')
        .annotate(value=Count('usuario_id', distinct=True))
        .order_by('rango')
    )
    bar_edad = [
        {'label': f"{r['rango']}-{r['rango']+9}", 'value': r['value']}
        for r in age_qs
    ]

    # ─────────── TORTA POR SEXO ───────────
    sexo_avg_qs = (
        top_qs
        .values('usuario__sexo')
        .annotate(value=Avg('porcentaje'))
        .order_by('usuario__sexo')
    )
    pie_sexo = [
        {
            'label': 'Hombres' if r['usuario__sexo'] == 'M' else 'Mujeres',
            'value': round(r['value'], 1)
        }
        for r in sexo_avg_qs
    ]

    # ─────────── TORTA POR REGIÓN ───────────
    region_avg_qs = (
        top_qs
        .exclude(usuario__region='')
        .values('usuario__region')
        .annotate(value=Avg('porcentaje'))
        .order_by('usuario__region')
    )
    pie_region = [
        {
            'label': r['usuario__region'],
            'value': round(r['value'], 1)
        }
        for r in region_avg_qs
    ]

    # ─────────── TORTA POR RANGO ETARIO ───────────
    age_avg_qs = (
        top_qs
        .filter(usuario__edad__gte=18)
        .annotate(
            rango=ExpressionWrapper(
                Floor(F('usuario__edad') / Value(10.0)) * Value(10),
                output_field=IntegerField()
            )
        )
        .values('rango')
        .annotate(value=Avg('porcentaje'))
        .order_by('rango')
    )
    pie_edad = [
        {
            'label': f"{r['rango']}-{r['rango']+9}",
            'value': round(r['value'], 1)
        }
        for r in age_avg_qs
    ]

    # ④ JSON plano para filtros combinados (sexo / edad / región)
    pref_data = list(
        top_qs.values(
            candidato_nombre=F('candidato__nombre'),
            sexo=F('usuario__sexo'),
            edad=F('usuario__edad'),
            region=F('usuario__region'),
        )
    )

    # ─────────────── Render ────────────────────────────────
    return render(request, 'dashboard.html', {
        'total'        : total_users,
        'bar_general'  : bar_general,
        'pie_general'  : pie_general,
        'bar_sexo'     : bar_sexo,
        'bar_region'   : bar_region,
        'bar_edad'     : bar_edad,
        'pie_sexo'     : pie_sexo,
        'pie_region'   : pie_region,
        'pie_edad'     : pie_edad,
        'pref_data'    : pref_data,
    })


 
@login_required
def change_email(request):
    """
    Vista simplificada para cambiar el correo del usurio de forma inmediata,
    sin confirmaciones por token. Actualiza tanto User.email como Usuario.email.
    """
    if request.method == 'POST':
        form = EmailChangeForm(request.user, data=request.POST)
        if form.is_valid():
            # 1) Toma el nuevo correo validado
            new_email = form.cleaned_data['new_email']

            # 2) Actualiza el User estándar
            request.user.email = new_email
            request.user.save()

            # 3) Actualiza tu modelo Usuario (perfil extendido)
            perfil = Usuario.objects.get(rut=request.user.username)
            perfil.email = new_email
            perfil.save()

            messages.success(request, 'Tu correo ha sido actualizado con éxito.')
            return redirect('configuracion')
        else:
            messages.error(request, 'Corrige los errores antes de continuar.')
    else:
        form = EmailChangeForm(request.user)

    return render(request, 'change_email.html', {'form': form})

@login_required
def confirm_change_email(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and email_change_token.check_token(user, token):
        new_email = request.session.get('new_email')
        if new_email:
            user.email = new_email
            user.save()
            del request.session['new_email']
            messages.success(request, 'Tu correo ha sido actualizado con éxito.')
            return redirect('configuracion')

    messages.error(request, 'El enlace no es válido o ha expirado.')
    return redirect('configuracion')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
            return redirect('configuracion')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
def configuracion(request):
    # 1) perfil extendido
    usuario = Usuario.objects.get(rut=request.user.username)

    # 2) instanciar formularios con prefijos
    email_form = EmailChangeForm(
        user=request.user,
        data=request.POST or None,
        prefix='email'
    )
    pwd_form = CustomPasswordChangeForm(
        user=request.user,
        data=request.POST or None,
        prefix='pwd'
    )

    if request.method == 'POST':
        # ─── Cambiar correo electrónico ─────────────────────────────
        if 'email-submit' in request.POST:
            if email_form.is_valid():
                nuevo = email_form.cleaned_data['new_email']
                # ① actualizar en auth.User
                request.user.email = nuevo
                request.user.save()
                # ② actualizar en tu perfil extendido
                usuario.email = nuevo
                usuario.save()
                messages.success(request, 'Tu correo ha sido actualizado con éxito.')
                return redirect('configuracion')
            else:
                messages.error(request, 'Corrige los errores del formulario de correo.')

        # ─── Cambiar contraseña ──────────────────────────────────────
        elif 'pwd-submit' in request.POST:
            if pwd_form.is_valid():
                user = pwd_form.save()
                update_session_auth_hash(request, user)  # no cerrar sesión
                messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
                return redirect('configuracion')
            else:
                messages.error(request, 'Corrige los errores del formulario de contraseña.')

        # ─── Eliminar cuenta ─────────────────────────────────────────
        elif 'delete-submit' in request.POST:
            pwd = request.POST.get('delete-password','')
            if not request.user.check_password(pwd):
                messages.error(request, 'Contraseña incorrecta. No se eliminó tu cuenta.')
            else:
                # borrar perfil extendido
                Usuario.objects.filter(rut=request.user.username).delete()
                # cerrar sesión y borrar User
                logout(request)
                request.user.delete()
                messages.success(request, 'Tu cuenta ha sido eliminada correctamente.')
                return redirect('home')

    return render(request, 'config.html', {
        'usuario'    : usuario,
        'email_form' : email_form,
        'pwd_form'   : pwd_form,
    })

@login_required
def confirmar_cambio_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_change_token.check_token(user, token):
        nuevo_email = request.session.get('nuevo_email')
        if nuevo_email:
            user.email = nuevo_email
            user.save()
            del request.session['nuevo_email']
            messages.success(request, 'Correo electrónico actualizado correctamente.')
            return redirect('configuracion')

    messages.error(request, 'El enlace de confirmación no es válido o ha expirado.')
    return redirect('configuracion')


@login_required
def delete_account(request):
    if request.method == 'POST':
        auth_user = request.user
        # ① borra el perfil extendido
        Usuario.objects.filter(rut=auth_user.username).delete()
        # ② cierra sesión y borra el User
        logout(request)
        auth_user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('home')
    return render(request, 'delete_account.html')

@login_required
def mi_perfil(request):
    usuario = Usuario.objects.get(rut=request.user.username)
    regiones = [
        'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo',
        'Valparaíso', 'Metropolitana', 'O’Higgins', 'Maule', 'Ñuble',
        'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes'
    ]

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('mi_perfil')
    else:
        form = PerfilForm(instance=usuario)

    return render(request, 'miperfil.html', {
        'form': form,
        'usuario': usuario,
        'regiones': regiones
    })

def home(request):
    nombre_usuario = None
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(rut=request.user.username)
            nombre_usuario = usuario.nombre
        except Usuario.DoesNotExist:
            pass
    return render(request, 'home.html', {'nombre_usuario': nombre_usuario})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # aquí el rut ya es único
            user = User.objects.create_user(
                username=cd['rut'],
                email=cd['email'],
                password=cd['password1']
            )
            Usuario.objects.create(
                rut        = cd['rut'],
                nombre     = cd['nombre'],
                email      = cd['email'],
                contraseña = user.password,
                edad       = cd['edad'],
                region     = cd['region'],
                sexo       = cd['sexo']
            )
            messages.success(request, 'Te has registrado con éxito. Inicia sesión para continuar.')
            return redirect('signin')
        else:
            messages.error(request, 'Revisa los errores del formulario.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Error al crear la tarea'
            })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error al editar la tarea'
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def cuestionario(request):
    usuario = Usuario.objects.get(rut=request.user.username)

    # ── (a) reinicio forzado ────────────────────────────────────────
    if request.GET.get("new") == "1":
        RespuestaUsuario.objects.filter(usuario=usuario).delete()
        Afinidad.objects.filter(usuario=usuario).delete()

    # ── (b) si ya respondió → mostrar resultado “afinidad” ──────────
    if (
        request.method == "GET"
        and RespuestaUsuario.objects.filter(usuario=usuario).exists()
    ):
        afinidades = (
    Afinidad.objects
    .filter(usuario=usuario)
    .select_related("candidato")
    # .order_by("-porcentaje")  ← quítalo o deja el orden al final
)

        # lista básica
        resultados = [
            {"nombre": a.candidato.nombre, "pct": float(a.porcentaje)}
            for a in afinidades
        ]

        # ── NUEVO: marcar los máximos (puede haber empate) ──────────────
        if resultados:
            max_pct = max(r["pct"] for r in resultados)
            for r in resultados:
                r["top"] = r["pct"] == max_pct     

        # (opcional) ordenar ahora:
        resultados.sort(key=lambda r: r["pct"], reverse=True)

        return render(
            request,
            "cuestionario.html",
            {
                "resultados"    : resultados, 
                "ya_respondido" : True,
            },
        )

    # ── (c) POST: guardar respuestas y calcular afinidad ────────────
    if request.method == "POST":
        suma = {}              
        respondidas = set()     # para contar cuántas preguntas respondió

        for k, v in request.POST.items():
            if not k.startswith("pregunta_"):
                continue

            q_id = k.split("_", 1)[1]
            respondidas.add(q_id)

            alternativa = get_object_or_404(Alternativa, pk=v, pregunta_id=q_id)

            # guarda / actualiza la respuesta del usuario
            RespuestaUsuario.objects.update_or_create(
                usuario=usuario,
                pregunta_id=q_id,
                defaults={"alternativa": alternativa},
            )

            # acumula ponderaciones
            for p in alternativa.ponderaciones.all():
                suma[p.candidato] = suma.get(p.candidato, 0) + p.peso

        base = max(len(respondidas) * 10, 1)   # evita división cero

        # porcentaje redondeado y ordenado ↓↓↓
        resultados_ordenados = sorted(
            (
                (cand, round((peso / base) * 100, 1))
                for cand, peso in suma.items()
            ),
            key=lambda t: t[1],
            reverse=True
        )

        with transaction.atomic():
            for cand, pct in resultados_ordenados:
                Afinidad.objects.update_or_create(
                    usuario   = usuario,
                    candidato = cand,
                    defaults  = {"porcentaje": pct},
                )

        messages.success(request, "✅ Tus respuestas se han registrado.")
        return redirect("cuestionario")             # patrón PRG

    # ── (d) GET inicial: 11 preguntas aleatorias ────────────────────
    preguntas = list(Pregunta.objects.order_by("?")[:11])
    preguntas_data = [
        {
            "pregunta"    : p,
            "alternativas": list(p.alternativa_set.order_by("?"))
        }
        for p in preguntas
    ]

    return render(
        request,
        "cuestionario.html",
        {
            "preguntas_data": preguntas_data,
            "ya_respondido" : False,
            "resultados"    : [],
        },
    )
    
    
@login_required
def micuestionario(request):
    usuario = Usuario.objects.get(rut=request.user.username)

    # ① traer respuestas y afinidades
    respuestas = RespuestaUsuario.objects.filter(usuario=usuario).order_by('-id')
    afinidades = Afinidad.objects.filter(usuario=usuario).order_by('-porcentaje')

    # ② preparar datos para radar
    # Lista de TODOS los candidatos (en el orden de la BD)
    nombres_ref = list(Candidato.objects.values_list('nombre', flat=True))
    # Mapa nombre→% del usuario
    afin_map = { a.candidato.nombre: float(a.porcentaje) for a in afinidades }
    # Array completo rellenando con 0%
    radar_data = [
        {"nombre": n, "pct": afin_map.get(n, 0.0)}
        for n in nombres_ref
    ]

    return render(request, 'micuestionario.html', {
        'respuestas' : respuestas,
        'afinidades' : afinidades,
        # PASA la lista, no el string:
        'radar_data' : radar_data,
    })
