from flask import Flask, request, jsonify, render_template
import sqlite3
import gradio as gr

app = Flask(__name__)

# Function to initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS tasks')  # Drop the existing table if it exists
        c.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                priority TEXT NOT NULL DEFAULT 'low'
            )
        ''')  # Create the tasks table
        conn.commit()

# Reusable function to execute a query
def execute_query(query, params=()):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()

# Reusable function to fetch all results from a query
def fetch_all(query, params=()):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute(query, params)
        return c.fetchall()

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the to-do list page
@app.route('/todo')
def todo():
    return render_template('todo.html')

# Route to get all to-do tasks
@app.route('/todos', methods=['GET'])
def get_todos():
    tasks = fetch_all('SELECT * FROM tasks')
    return jsonify([{"id": task[0], "task": task[1], "status": task[2], "priority": task[3]} for task in tasks])

# Route to add a new to-do task
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    task = data.get('task')
    priority = data.get('priority')
    if not task or not priority:
        return jsonify({"message": "Invalid data"}), 400
    execute_query('INSERT INTO tasks (task, priority) VALUES (?, ?)', (task, priority))
    return jsonify({"message": "Task added successfully!"})

# Route to delete a to-do task
@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    execute_query('DELETE FROM tasks WHERE id = ?', (task_id,))
    return jsonify({"message": "Task deleted successfully!"})

# Route to update the status and priority of a to-do task
@app.route('/todos/<int:task_id>', methods=['PUT'])
def update_todo_status(task_id):
    data = request.json
    status = data.get('status')
    priority = data.get('priority')
    execute_query('UPDATE tasks SET status = ?, priority = ? WHERE id = ?', (status, priority, task_id))
    return jsonify({"message": "Task status updated successfully!"})

# Route to render the contact form
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to handle contact form submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Here you can handle the form submission, e.g., save the data to a database or send an email
    return jsonify({"message": "Thank you for contacting us!"})

# Gradio Interface Functions
def add_task_interface(task, priority):
    execute_query('INSERT INTO tasks (task, priority) VALUES (?, ?)', (task, priority))
    return "Task added successfully!"

def get_tasks_interface():
    tasks = fetch_all('SELECT * FROM tasks')
    return "\n".join([f"ID: {task[0]}, Task: {task[1]}, Status: {task[2]}, Priority: {task[3]}" for task in tasks])

def delete_task_interface(task_id):
    execute_query('DELETE FROM tasks WHERE id = ?', (task_id,))
    return "Task deleted successfully!"

def update_task_status_interface(task_id, status, priority):
    execute_query('UPDATE tasks SET status = ?, priority = ? WHERE id = ?', (status, priority, task_id))
    return "Task status updated successfully!"

# Gradio Interfaces
add_task_iface = gr.Interface(
    fn=add_task_interface,
    inputs=[gr.Textbox(label="Task"), gr.Textbox(label="Priority (low/medium/high)")],
    outputs=gr.Textbox(label="Result")
)

view_tasks_iface = gr.Interface(
    fn=get_tasks_interface,
    inputs=None,
    outputs=gr.Textbox(label="Tasks")
)

delete_task_iface = gr.Interface(
    fn=delete_task_interface,
    inputs=gr.Textbox(label="Task ID"),
    outputs=gr.Textbox(label="Result")
)

update_task_status_iface = gr.Interface(
    fn=update_task_status_interface,
    inputs=[gr.Textbox(label="Task ID"), gr.Textbox(label="Status (pending/completed)"), gr.Textbox(label="Priority (low/medium/high)")],
    outputs=gr.Textbox(label="Result")
)

# Combine Gradio Interfaces into a Tabbed Interface
iface = gr.TabbedInterface(
    [add_task_iface, view_tasks_iface, delete_task_iface, update_task_status_iface],
    ["Add Task", "View Tasks", "Delete Task", "Update Task Status"]
)

# Route to launch the Gradio interface
@app.route('/gradio')
def gradio_interface():
    return iface.launch(share=True)

# Initialize the database
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Ensure Flask runs on port 5000
   
   
   
    
    
    
    