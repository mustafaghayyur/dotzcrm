import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from tasks.drm.crud import Tasks, WorkSpaces

class TasksListApiOps(APITestCase):
    """
    Test for the universal list API node (restapi.views.list)
    to ensure it can properly fetch Task records based on various criteria.
    """

    def setUp(self):
        # Create users for ownership and assignment tests
        User = get_user_model()
        self.user1 = User.objects.create_user(username='testuser1', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password')
        self.client.force_authenticate(user=self.user1)

        # The universal list API endpoint
        self.url = '/rest/all/'

        # DRM CRUD instances for data setup
        self.tasksCrud = Tasks(current_user=self.user1)
        self.wsCrud = WorkSpaces(current_user=self.user1)

        # Create a workspace to associate with some tasks
        self.workspace = self.wsCrud.create({
            'name': 'Test Workspace For List API',
            'description': 'A test workspace.',
            'type': 'private',
            'creator_id': self.user1.id
        })

        # Create 5 task records with varying attributes for comprehensive testing
        now = datetime.datetime.now(datetime.timezone.utc)
        self.tasksCrud.create({
            'description': 'Task 1 private visibility',
            'status': 'created',
            'visibility': 'private',
            'deadline': now + datetime.timedelta(days=2),
            'creator_id': self.user1.id,
            'assignee_id': self.user1.id,
            'assignor_id': self.user2.id
        })
        self.tasksCrud.create({
            'description': 'Task 2 workspace visibility',
            'status': 'started',
            'visibility': 'workspaces',
            'deadline': now + datetime.timedelta(days=10),
            'creator_id': self.user1.id,
            'assignee_id': self.user2.id,
            'assignor_id': self.user1.id,
            'workspace_id': self.workspace.id
        })
        self.tasksCrud.create({
            'description': 'Task 3 also private',
            'status': 'created',
            'visibility': 'private',
            'deadline': now + datetime.timedelta(days=5),
            'creator_id': self.user2.id,
            'assignee_id': self.user1.id,
            'assignor_id': self.user2.id
        })
        self.tasksCrud.create({
            'description': 'Task 4 another workspace task',
            'status': 'completed',
            'visibility': 'workspaces',
            'deadline': now + datetime.timedelta(days=20),
            'creator_id': self.user2.id,
            'assignee_id': self.user2.id,
            'assignor_id': self.user1.id,
            'workspace_id': self.workspace.id
        })
        self.tasksCrud.create({
            'description': 'Task 5 for special text search',
            'status': 'onhold',
            'visibility': 'private',
            'deadline': now + datetime.timedelta(days=30),
            'creator_id': self.user1.id,
            'assignee_id': self.user1.id,
            'assignor_id': self.user2.id
        })

    def oneAllTasks(self):
        """
        Test retrieving all non-deleted tasks. Should be 5.
        """
        payload = {
            'tbl': 'tata',
            'selectors': ['tata_id', 'description', 'status', 'visibility', 'deadline', 'creator_id', 'assignee_id', 'workspace_id'],
            'conditions': {'delete_time': 'IS NULL'},
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response: {response.content.decode()}")
        
        body = response.json()
        data = body.get('results')
        self.assertIsInstance(data, list, "Read operation should return a list of records")
        self.assertEqual(len(data), 5, "Should retrieve all 5 created tasks")

    def twoFilterByVisibility(self):
        """
        Test searching for tasks with 'private' visibility. Should find 3.
        """
        payload = {
            'tbl': 'tata',
            'selectors': ['tata_id', 'description', 'status', 'visibility', 'deadline', 'creator_id', 'assignee_id', 'workspace_id'],
            'conditions': {'visibility': 'private'}
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response: {response.content.decode()}")
        body = response.json()
        data = body.get('results')
        self.assertIsInstance(data, list, "Read operation should return a list of records")
        self.assertEqual(len(data), 3, "Should find 3 private tasks")
        for task in data:
            self.assertEqual(task['visibility'], 'private')

    def threeFilterByDeadline(self):
        """
        Test searching for tasks with a deadline between now and 15 days from now. Should find 3.
        """
        now = datetime.datetime.now(datetime.timezone.utc).date()
        futureDate = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=15)).date()
        payload = {
            'tbl': 'tata',
            'conditions': {'deadline': f'from {now} to {futureDate}'}
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response: {response.content.decode()}")
        body = response.json()
        data = body.get('results')
        self.assertIsInstance(data, list, "Read operation should return a list of records")
        self.assertEqual(len(data), 3, "Should find 3 tasks with a deadline > 15 days")

    def fourFilterByWorkspace(self):
        """
        Test searching for tasks associated with a specific workspace. Should find 2.
        """
        payload = {
            'tbl': 'tata',
            'conditions': {'workspace_id': self.workspace.id}
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response: {response.content.decode()}")
        body = response.json()
        data = body.get('results')
        self.assertIsInstance(data, list, "Read operation should return a list of records")
        self.assertEqual(len(data), 2, "Should find 2 tasks in the specified workspace")

    def fiveFreeTextSearch(self):
        """
        Test free-text search on the description field. Should find 1.
        NOTE: This assumes the backend supports a Django-style '__icontains' lookup.
        """
        payload = {
            'tbl': 'tata',
            'conditions': {'description__icontains': 'special text'}
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response: {response.content.decode()}")
        body = response.json()
        data = body.get('results')
        self.assertIsInstance(data, list, "Read operation should return a list of records")
        self.assertEqual(len(data), 1, "Should find 1 task via free-text search")
        self.assertEqual(data[0]['description'], 'Task 5 for special text search')