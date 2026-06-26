from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', verbose_name="Usuario")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    company = models.CharField(max_length=255, blank=True, verbose_name="Empresa")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('on_hold', 'En espera'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects', verbose_name="Cliente")
    name = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Estado")
    start_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Fin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]
    STATUS_CHOICES = [
        ('todo', 'Pendiente'),
        ('doing', 'En progreso'),
        ('done', 'Hecho'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name="Proyecto")
    name = models.CharField(max_length=255, verbose_name="Tarea")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridad")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo', verbose_name="Estado")
    due_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Entrega")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return self.name
