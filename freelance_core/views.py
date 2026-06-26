from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .models import Client, Project, Task
from .serializers import ClientSerializer, ProjectSerializer, TaskSerializer

# --- Vistas de la API (DRF) ---

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(client__user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__client__user=self.request.user)

# --- Vistas del Dashboard e Interfaz (HTMX) ---

@method_decorator(login_required, name='dispatch')
class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        user = request.user
        clients_count = Client.objects.filter(user=user).count()
        active_projects = Project.objects.filter(client__user=user, status='active').count()
        
        data = {
            'clients_count': clients_count,
            'active_projects': active_projects,
        }
        
        if request.accepted_renderer.format == 'html':
            return render(request, 'dashboard.html', data)
        return Response(data)

@login_required
@require_http_methods(["GET"])
def client_edit_view(request, pk):
    client = Client.objects.get(pk=pk, user=request.user)
    return render(request, 'client_edit.html', {'client': client})

@login_required
@require_http_methods(["POST"])
def client_update_view(request, pk):
    client = Client.objects.get(pk=pk, user=request.user)
    client.name = request.POST.get('name')
    client.email = request.POST.get('email')
    client.company = request.POST.get('company', '')
    client.save()
    return redirect('client_list')

@login_required
@require_http_methods(["GET"])
def project_edit_view(request, pk):
    project = Project.objects.get(pk=pk, client__user=request.user)
    clients = Client.objects.filter(user=request.user)
    return render(request, 'project_edit.html', {'project': project, 'clients': clients})

@login_required
@require_http_methods(["POST"])
def project_update_view(request, pk):
    project = Project.objects.get(pk=pk, client__user=request.user)
    project.client_id = request.POST.get('client_id')
    project.name = request.POST.get('name')
    project.description = request.POST.get('description', '')
    project.status = request.POST.get('status')
    project.save()
    return redirect('project_list')

@login_required
@require_http_methods(["GET"])
def client_list_view(request):
    clients = Client.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'clients.html', {'clients': clients})

@login_required
@require_http_methods(["POST"])
def client_create_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    company = request.POST.get('company', '')
    
    client = Client.objects.create(
        user=request.user,
        name=name,
        email=email,
        company=company
    )
    return render(request, 'partials/client_row.html', {'client': client})

@login_required
@require_http_methods(["DELETE"])
def client_delete_view(request, pk):
    try:
        client = Client.objects.get(pk=pk, user=request.user)
        client.delete()
    except Client.DoesNotExist:
        pass
    return HttpResponse("")

@login_required
@require_http_methods(["GET"])
def project_list_view(request):
    projects = Project.objects.filter(client__user=request.user).order_by('-created_at')
    clients = Client.objects.filter(user=request.user)
    return render(request, 'projects.html', {'projects': projects, 'clients': clients})

@login_required
@require_http_methods(["POST"])
def project_create_view(request):
    client_id = request.POST.get('client_id')
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    
    client = Client.objects.get(pk=client_id, user=request.user)
    project = Project.objects.create(
        client=client,
        name=name,
        description=description
    )
    return render(request, 'partials/project_row.html', {'project': project})

@login_required
@require_http_methods(["DELETE"])
def project_delete_view(request, pk):
    try:
        project = Project.objects.get(pk=pk, client__user=request.user)
        project.delete()
    except Project.DoesNotExist:
        pass
    return HttpResponse("")

@login_required
@require_http_methods(["GET"])
def task_kanban_view(request):
    tasks = Task.objects.filter(project__client__user=request.user)
    projects = Project.objects.filter(client__user=request.user)
    
    context = {
        'todo_tasks': tasks.filter(status='todo'),
        'doing_tasks': tasks.filter(status='doing'),
        'done_tasks': tasks.filter(status='done'),
        'projects': projects,
    }
    return render(request, 'tasks_kanban.html', context)

@login_required
@require_http_methods(["POST"])
def task_create_view(request):
    project_id = request.POST.get('project_id')
    name = request.POST.get('name')
    priority = request.POST.get('priority', 'medium')
    due_date = request.POST.get('due_date')
    
    project = Project.objects.get(pk=project_id, client__user=request.user)
    task = Task.objects.create(
        project=project,
        name=name,
        priority=priority,
        due_date=due_date if due_date else None
    )
    return redirect('task_kanban')

@login_required
@require_http_methods(["POST"])
def task_update_status_view(request, pk):
    task = Task.objects.get(pk=pk, project__client__user=request.user)
    new_status = request.POST.get('status')
    if new_status in ['todo', 'doing', 'done']:
        task.status = new_status
        task.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('accept') == 'application/json':
        return HttpResponse(status=204)
    return redirect('task_kanban')

@login_required
@require_http_methods(["DELETE"])
def task_delete_view(request, pk):
    try:
        task = Task.objects.get(pk=pk, project__client__user=request.user)
        task.delete()
    except Task.DoesNotExist:
        pass
    return HttpResponse("")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
