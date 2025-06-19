from django.contrib import admin
from .models import Task
from django.contrib import admin
from .models import Candidato, Pregunta, Alternativa, Ponderacion


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

# Register your models here.

admin.site.register([Candidato, Pregunta, Alternativa, Ponderacion])
admin.site.register(Task, TaskAdmin)
