import pytest
from app import app, init_db, execute_query

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_index(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_add_todo(client):
    """Test adding a new to-do task."""
    response = client.post('/todos', json={'task': 'Test Task', 'priority': 'high'})
    assert response.status_code == 200
    assert b'Task added successfully!' in response.data

def test_add_todo_invalid_data(client):
    """Test adding a new to-do task with invalid data."""
    response = client.post('/todos', json={'task': '', 'priority': 'high'})
    assert response.status_code == 400  # Assuming your app returns 400 for invalid data
    assert b'Invalid data' in response.data

def test_get_todos(client):
    """Test retrieving all to-do tasks."""
    client.post('/todos', json={'task': 'Test Task', 'priority': 'high'})
    response = client.get('/todos')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['task'] == 'Test Task'

def test_update_todo_status(client):
    """Test updating the status and priority of a to-do task."""
    client.post('/todos', json={'task': 'Test Task', 'priority': 'high'})
    response = client.put('/todos/1', json={'status': 'completed', 'priority': 'medium'})
    assert response.status_code == 200
    assert b'Task status updated successfully!' in response.data

def test_delete_todo(client):
    """Test deleting a to-do task."""
    client.post('/todos', json={'task': 'Test Task', 'priority': 'high'})
    response = client.delete('/todos/1')
    assert response.status_code == 200
    assert b'Task deleted successfully!' in response.data

def test_contact_form_submission(client):
    """Test the contact form submission."""
    response = client.post('/submit_contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'This is a test message.'
    })
    assert response.status_code == 200
    assert b'Thank you for contacting us!' in response.data

def test_gradio_interface(client):
    """Test the Gradio interface."""
    response = client.get('/gradio')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data  # Check if the response contains HTML content