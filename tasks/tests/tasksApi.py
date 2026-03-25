import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from tasks.models import Task
from tasks.drm.crud import Tasks
from core.helpers.data import getter

class TasksApiOps(APITestCase):
    """
    Test for Tasks CRUD operations via the unified API endpoint.
    Tests Create, Read, Update, and Delete functionality using POST requests with 'reqType'.
    """

    def setUp(self):
        # Create a user for authentication
        User = get_user_model()
        self.user = User.objects.create_user(username='apiuser', password='password')
        self.client.force_authenticate(user=self.user)
        
        # The unified CRUD endpoint
        self.url = '/rest/all/crud/'
        
        # Standard submission data for creating a task
        self.submissionData = {
            'reqType': 'create',
            'tbl': 'tata',
            'description': 'API Test Task. This will bring the char count to 20.',
            'status': 'created',
            'visibility': 'private',
            'assignee_id': self.user.id,
            'assignor_id': self.user.id,
            'deadline': (datetime.datetime.now() + datetime.timedelta(days=5)).isoformat(),
            'details': 'Detailed description of the task via API. This will bring the char count to 40, or atleast I hope it will.',
            'creator_id': self.user.id,
        }

    def createTestTask(self):
        """Helper method to create a task via DRM for other tests."""
        crud = Tasks(current_user=self.user)
        task = crud.create({
            'description': 'API Test Task',
            'status': 'created',
            'visibility': 'private',
            'deadline': datetime.datetime.now() + datetime.timedelta(days=5),
            'details': 'Detailed description.',
            'creator_id': self.user.id
        })
        return task.id

    def oneCreate(self):
        """
        Test the creation of a new Task record via API.
        """
        response = self.client.post(self.url, self.submissionData, format='json')
        
        # 1. Verify API Response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Create failed with 400. Response: {response.content.decode()}")
        
        # 2. Verify in Database
        tasks = Task.objects.select(['tata_id', 'description', 'status', 'creator_id']).where({'description': 'API Test Task. This will bring the char count to 20.'}).fetch()
        self.assertIsNotNone(tasks, "Task should be created in the database")
        task = tasks[0]
        self.assertEqual(task.creator_id, self.user.id)
        self.assertEqual(task.status, 'created')

    def twoRead(self):
        """
        Test reading the Task record via API (reqType='read').
        """
        taskId = self.createTestTask()
        
        payload = {
            'reqType': 'read',
            'tbl': 'tata',
            'tata_id': taskId
        }
        
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        data = body.get('results', [])

        if isinstance(data, dict):
            data = [data]

        self.assertIsInstance(data, list, "Read operation should return a list of records")
        self.assertEqual(len(data), 1, "Read operation should return exactly one record")
        record = data[0]

        self.assertEqual(getter(record, 'description'), 'API Test Task')
        self.assertEqual(getter(record, 'status'), 'created')

    def threeUpdate(self):
        """
        Test updating an existing Task record via API (reqType='update').
        """
        taskId = self.createTestTask()
        
        payload = {
            'reqType': 'update',
            'tbl': 'tata',
            'tata_id': taskId,
            'description': 'Updated via API. This will bring the char count to 20.',
            'status': 'started'
        }
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Update failed with 400. Response: {response.content.decode()}")
        
        # Verify in Database
        tasks = Task.objects.select(['tata_id', 'description', 'status']).where({'tata_id': taskId}).fetch()

        self.assertTrue(tasks, "Task should be found in the database after update")
        task = tasks[0]
        self.assertEqual(task.description, 'Updated via API. This will bring the char count to 20.')
        self.assertEqual(task.status, 'started')

    def fourDelete(self):
        """
        Test deleting a Task record via API (reqType='delete').
        """
        taskId = self.createTestTask()
        
        payload = {
            'reqType': 'delete',
            'tbl': 'tata',
            'tata_id': taskId
        }
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify Database State (Soft Delete)
        task = Task.objects.get(id=taskId)
        self.assertIsNotNone(task.delete_time, "Task should have a delete_time set")
