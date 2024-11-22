import unittest
import json
from app import app, init_db, execute_query

class ToDoAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client and initialize the database before each test
        self.app = app.test_client()
        self.app.testing = True
        init_db()  # Initialize the database for testing

    def test_index(self):
        # Test the home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'To-Do List', response.data)

    def test_add_todo(self):
        # Test adding a new to-do task
        response = self.app.post('/todos', data=json.dumps({
            'task': 'Test Task',
            'priority': 'high'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task added successfully!', response.data)

    def test_get_todos(self):
        # Test retrieving all to-do tasks
        self.app.post('/todos', data=json.dumps({
            'task': 'Test Task',
            'priority': 'high'
        }), content_type='application/json')
        response = self.app.get('/todos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['task'], 'Test Task')

    def test_update_todo_status(self):
        # Test updating the status and priority of a to-do task
        self.app.post('/todos', data=json.dumps({
            'task': 'Test Task',
            'priority': 'high'
        }), content_type='application/json')
        response = self.app.put('/todos/1', data=json.dumps({
            'status': 'completed',
            'priority': 'medium'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task status updated successfully!', response.data)

    def test_delete_todo(self):
        # Test deleting a to-do task
        self.app.post('/todos', data=json.dumps({
            'task': 'Test Task',
            'priority': 'high'
        }), content_type='application/json')
        response = self.app.delete('/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task deleted successfully!', response.data)

    def test_add_todo_invalid_data(self):
        # Test adding a to-do task with invalid data
        response = self.app.post('/todos', data=json.dumps({
            'task': '',
            'priority': 'high'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Assuming you handle validation and return 400 for bad requests

    def test_update_todo_invalid_id(self):
        # Test updating a to-do task with an invalid ID
        response = self.app.put('/todos/999', data=json.dumps({
            'status': 'completed',
            'priority': 'medium'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 404)  # Assuming you return 404 for not found

    def test_contact_form_submission(self):
        # Test the contact form submission
        response = self.app.post('/submit_contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for contacting us!', response.data)

    def test_gradio_interface(self):
        # Test the Gradio interface route
        response = self.app.get('/gradio')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()