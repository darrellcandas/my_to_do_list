# My To-Do List Application

## Overview

This is a full-stack to-do list application built with Flask for the backend, Gradio for the frontend, and SQLite for the database. The application allows users to manage their tasks with CRUD (Create, Read, Update, Delete) operations, customize the appearance, and contact the developer.

## Features

- **Home Page**: Provides links to other pages.
- **To-Do List Page**: Allows users to add, view, update, and delete tasks. Users can also customize the appearance of the application.
- **Contact Page**: Allows users to send messages to the developer.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**:

    ```sh
    git clone https://github.com/darrellcandas/my_to_do_list
    cd my_to_do_list
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv env
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```sh
        .\env\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source env/bin/activate
        ```

4. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:

    ```sh
    python app.py
    ```

2. **Open your web browser** and navigate to `http://127.0.0.1:5000` to access the application.

## API Endpoints

- `GET /todos`: Retrieve all tasks.
- `POST /todos`: Add a new task.
- `PUT /todos/<int:task_id>`: Update the status and priority of a task.
- `DELETE /todos/<int:task_id>`: Delete a task.
- `GET /gradio`: Access the Gradio interface.

## Directory Structure


