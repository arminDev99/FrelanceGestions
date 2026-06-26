from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client, Project, Task

class RootDevTests(TestCase):
    def setUp(self):
        # Configuración inicial: Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Crear un cliente de prueba
        self.test_client = Client.objects.create(
            user=self.user,
            name='Cliente de Prueba',
            email='cliente@prueba.com',
            company='Empresa Test'
        )

    def test_client_creation(self):
        """Verifica que un cliente se cree correctamente vinculado a un usuario."""
        self.assertEqual(self.test_client.name, 'Cliente de Prueba')
        self.assertEqual(self.test_client.user.username, 'testuser')
        self.assertEqual(Client.objects.count(), 1)

    def test_project_creation(self):
        """Verifica que un proyecto se cree vinculado a un cliente."""
        project = Project.objects.create(
            client=self.test_client,
            name='Proyecto Alpha',
            description='Descripción del proyecto alpha',
            status='active'
        )
        self.assertEqual(project.name, 'Proyecto Alpha')
        self.assertEqual(project.client.name, 'Cliente de Prueba')
        self.assertEqual(Project.objects.count(), 1)

    def test_task_creation(self):
        """Verifica que una tarea se cree vinculada a un proyecto con su prioridad."""
        project = Project.objects.create(client=self.test_client, name='Proyecto Beta')
        task = Task.objects.create(
            project=project,
            name='Tarea Crítica',
            priority='high',
            status='todo'
        )
        self.assertEqual(task.name, 'Tarea Crítica')
        self.assertEqual(task.priority, 'high')
        self.assertEqual(task.project.name, 'Proyecto Beta')
        self.assertEqual(Task.objects.count(), 1)

    def test_cascade_deletion(self):
        """Verifica que al borrar un cliente, sus proyectos y tareas se borren (Integridad)."""
        project = Project.objects.create(client=self.test_client, name='Proyecto a borrar')
        Task.objects.create(project=project, name='Tarea a borrar')
        
        # Borrar cliente
        self.test_client.delete()
        
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)

    def test_login_required_redirect(self):
        """Verifica que las páginas protegidas redirijan al login si no hay sesión."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_successful_login(self):
        """Verifica que un usuario pueda iniciar sesión correctamente."""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302) # Redirección tras login exitoso
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_registration(self):
        """Verifica que el formulario de registro cree un nuevo usuario."""
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123' 
        })

        user_exists = User.objects.filter(username='newuser').exists()
  
        
        response = self.client.post('/register/', {
            'username': 'realnewuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertTrue(User.objects.filter(username='realnewuser').exists())
