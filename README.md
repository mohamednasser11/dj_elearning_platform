
# Django backend (CS Graduation project)

Welcome to the backend project! Please follow these steps to set up the environment and install the required dependencies.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher**: Required to run the Django application.
- **PostgreSQL 16 or higher**: Required as the database for this project.
- **Ollama 0.9.0 or higher with gemma3**: Required to run the AI.

## 1. Create a New Virtual Environment

After pulling the project, you need to create a new virtual environment for the Python project.

### Steps:
1. Open your terminal or command prompt.
2. Navigate to the project directory where you have pulled the project.
   
   ```bash
   cd path/to/your/project
   ```

3. Create a new virtual environment:

   - On **Windows**:
     ```bash
     python -m venv venv
     ```
   - On **MacOS/Linux**:
     ```bash
     python3 -m venv venv
     ```

   This will create a new virtual environment folder called `venv` in your project directory.

## 2. Activate the Virtual Environment

Now that you've created the virtual environment, you need to activate it.

### Steps:
- On **Windows**:
  ```bash
  source venv/Scripts/activate
  ```

- On **MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

You should now see the name of your virtual environment in the terminal (e.g., `(venv)`).

## 3. Install Required Dependencies

Once the virtual environment is activated, you can install all the required dependencies for the project.

### Steps:
1. Make sure your `requirements.txt` file is in the root of the project directory.
2. Install the dependencies:

   - On **Windows** or **MacOS/Linux**:
     ```bash
     pip install -r requirements.txt
     ```

This will install all the required libraries listed in `requirements.txt`.

## 4. Generate the Postgres database

we will need to communicate with each other in order to keep up with the models migrations once you are notified that there is a new change in the models please migrate your database tables to the latest

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Start Django app

To start your django server use the following commands

```bash
   daphne e_learning_platform.asgi:application --port 8000
```

## 6. Deactivate the Virtual Environment

Once you're done working, you can deactivate the virtual environment by simply running:

```bash
deactivate
```

---

That's it! You are all set up to work with the project. Let me know if you run into any issues.


## Websocket close codes

- `4000`: missing token
- `4001`: invalid token
- `4002`: user is unauthorized
- `4003`: invalid binary data format
- `4004`: received message is empty
- `4005`: invalid JSON format
- `4006`: received message does not provide type
- `4007`: received message type is invalid
- `4008`: received message does not provide data
- `4009`: received message data does not provide message
- `4010`: tried to cancel a task that doesn't exist
- `4011`: course does not exist
- `4012`: session does not exist
- `4013`: user not enrolled to the course
- `5000`: unknown
