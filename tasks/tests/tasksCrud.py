import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.drm.crud import Tasks
from tasks.models import Task
from core.helpers.data import getter

class TasksCrudOps(TestCase):
    """
    Complete test for Tasks CRUD operations using the DRM layer and actual models.
    Tests Create, Read, Update, and Delete functionality.
    """

    def setUp(self):
        # Create a user to associate with tasks (required for creator_id)
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Initialize the Tasks CRUD class
        self.crud = Tasks(current_user=self.user)
        
        # Standard submission data for creating a task
        self.submissionData = {
            'description': 'Test Task Description',
            'status': 'created',
            'visibility': 'private',
            'deadline': datetime.datetime.now() + datetime.timedelta(days=5),
            'details': 'Detailed description of the task.',
            'creator_id': self.user.id,
        }

    def createTestTask(self):
        """Helper method to create a task for other tests."""
        self.crud.create(self.submissionData)
        return Task.objects.get(description='Test Task Description').id

    def oneCreate(self):
        """
        Test the creation of a new Task record.
        """
        # 1. Execute Create
        self.crud.create(self.submissionData)
        
        # 2. Verify in Database
        task = Task.objects.filter(description='Test Task Description').first()
        self.assertIsNotNone(task, "Task should be created in the database")
        self.assertEqual(task.creator_id, self.user.id)
        self.assertEqual(task.description, 'Test Task Description')

    def twoRead(self):
        """
        Test reading the Task record using fullRecord().
        """
        # Setup
        taskId = self.createTestTask()
        
        # Execute Read
        results = self.crud.fullRecord(taskId)
        
        # Verify
        self.assertIsNotNone(results, "fullRecord should return data")
        self.assertGreater(len(results), 0, "Should find at least one record")
        
        record = results[0]
        self.assertEqual(getter(record, 'description'), 'Test Task Description')
        self.assertEqual(getter(record, 'status'), 'created')
        self.assertEqual(getter(record, 'visibility'), 'private')

    def threeUpdate(self):
        """
        Test updating an existing Task record.
        """
        # Setup
        taskId = self.createTestTask()
        
        updateData = {
            'tata_id': taskId,
            'description': 'Updated Description',
            'status': 'started',
            'details': 'Updated details text.'
        }
        
        # Execute Update
        self.crud.update(updateData)
        
        # Verify in Database (Master Record)
        task = Task.objects.get(id=taskId)
        self.assertEqual(task.description, 'Updated Description')
        
        # Verify via Read (checks joined children data)
        results = self.crud.fullRecord(taskId)
        record = results[0]
        self.assertEqual(getter(record, 'description'), 'Updated Description')
        self.assertEqual(getter(record, 'status'), 'started')
        self.assertEqual(getter(record, 'details'), 'Updated details text.')

    def fourDelete(self):
        """
        Test deleting (soft delete) a Task record.
        """
        # Setup
        taskId = self.createTestTask()
        
        # Execute Delete
        self.crud.delete(taskId)
        
        # Verify Database State (Soft Delete)
        task = Task.objects.get(id=taskId)
        self.assertIsNotNone(task.delete_time, "Task should have a delete_time set (soft delete)")
        
        # Verify Read Logic (Should filter out deleted)
        results = self.crud.fullRecord(taskId)
        if results:
            self.assertEqual(len(results), 0, "Deleted task should not be returned by fullRecord")
        else:
            self.assertIsNone(results)