
from django.contrib import admin
from tasks import views
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [

    path(
    "reset-password/",
    auth_views.PasswordResetView.as_view(
      template_name="recuperar/password_reset_form.html",
      email_template_name="recuperar/password_reset_email.html",
      subject_template_name="recuperar/password_reset_subject.txt",
      success_url=reverse_lazy("password_reset_done"),
    ),
    name="password_reset",
    ),
    path(
        "reset-password/done/",
        auth_views.PasswordResetDoneView.as_view(
        template_name="recuperar/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
        template_name="recuperar/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        auth_views.PasswordResetCompleteView.as_view(
        template_name="recuperar/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    path('preguntas/',                views.pregunta_list,   name='pregunta_list'),
    path('preguntas/nueva/',          views.pregunta_create, name='pregunta_create'),
    path('preguntas/<int:pk>/editar/',   views.pregunta_update, name='pregunta_update'),
    path('preguntas/<int:pk>/eliminar/', views.pregunta_delete, name='pregunta_delete'),

    path('admin/', admin.site.urls),
    path('como-funciona/', views.como_funciona, name='como_funciona'),
    path('candidatos/', views.candidatos, name='candidatos'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('config/correo/confirmar/<uidb64>/<token>/',
         views.confirm_change_email,
         name='confirm_change_email'),
    path('confirmar-cambio-email/<uidb64>/<token>/', views.confirmar_cambio_email, name='confirmar_cambio_email'),
    path('configuracion/cambiar-contrasena/', views.change_password, name='change_password'),
    path('configuracion/cambiar-correo/', views.change_email, name='change_email'),
    path('configuracion/eliminar-cuenta/', views.delete_account, name='delete_account'),
    path('', views.home, name='home'),
    path('micuestionario/', views.micuestionario, name='micuestionario'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('miperfil/', views.mi_perfil, name='mi_perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('cuestionario/', views.cuestionario, name='cuestionario'),
    path('signin/', views.signin, name='signin')
]
