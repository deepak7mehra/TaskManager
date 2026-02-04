from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Task

class TaskManagerTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="regular_user", 
            password="password123", 
            role="regular",
            email="regular@test.com"
        )
        self.admin_user = User.objects.create_user(
            username="admin_user", 
            password="password123", 
            role="admin",
            email="admin@test.com"
        )
        
        self.task = Task.objects.create(
            user=self.user, 
            title="User Task", 
            description="Owned by regular user"
        )

        self.login_url = reverse('token_obtain_pair')
        self.task_list_url = reverse('task-list')
        self.task_detail_url = reverse('task-detail', kwargs={'pk': self.task.id})

    def get_token(self, username, password):
        """Helper to get a JWT token"""
        response = self.client.post(self.login_url, {"username": username, "password": password})
        return response.data['access']

    # --- AUTHENTICATION TESTS ---
    def test_registration(self):
        url = reverse('register')
        data = {"username": "new_guy", "password": "securepassword", "email": "new@test.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # --- TASK CRUD TESTS ---
    def test_create_task(self):
        token = self.get_token("regular_user", "password123")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {"title": "New Task", "description": "Doing my homework"}
        response = self.client.post(self.task_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 2)

    def test_unauthorized_access(self):
        """Should fail if no token is provided"""
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- ROLE & PRIVACY TESTS ---
    def test_regular_user_privacy(self):
        """Regular user should NOT see admin's tasks (if any)"""
        Task.objects.create(user=self.admin_user, title="Secret Admin Task")
        token = self.get_token("regular_user", "password123")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.task_list_url)
        self.assertEqual(len(response.data['results']), 1)

    def test_admin_sees_everything(self):
        """Admin role should see all tasks from all users"""
        token = self.get_token("admin_user", "password123")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.task_list_url)
        self.assertGreaterEqual(len(response.data['results']), 1)

    # --- FILTERING & PAGINATION ---
    def test_filtering_completed(self):
        Task.objects.create(user=self.user, title="Done Task", completed=True)
        token = self.get_token("regular_user", "password123")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get(f"{self.task_list_url}?completed=true")
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue(response.data['results'][0]['completed'])

    def test_pagination(self):
        for i in range(6):
            Task.objects.create(user=self.user, title=f"Task {i}")
        
        token = self.get_token("regular_user", "password123")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.task_list_url)

        self.assertIn('next', response.data)
        self.assertEqual(len(response.data['results']), 5)