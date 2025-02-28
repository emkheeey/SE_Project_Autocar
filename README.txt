# AutoCar: Toyota Car Finder and Management System

## Project Overview
This project is a Django-based application for managing and finding Toyota cars. It includes user authentication and registration features.

## If you don't know what bash means, ignore it. Just mind the commands. Thank you.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/emkheeey/SE_Project_Autocar.git
   cd SE_Project_Autocar
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Starting the Server
To start the development server, run:
```bash
python manage.py runserver
```
Then open your browser and go to `http://127.0.0.1:8000/`.

## Database Migrations
To apply database migrations, use the following command:
```bash
python manage.py migrate
```
To create new migrations after making changes to models, run:
```bash
python manage.py makemigrations
```

## Adding New Templates
New templates should be added to the `templates` directory. Ensure that the template files have a `.html` extension and are linked correctly in your views.

## Key Files and Their Purpose
- `manage.py`: A command-line utility for interacting with the Django project.
- `settings.py`: Contains project settings and configurations.
- `urls.py`: Defines URL patterns for the application.
- `views.py`: Contains the logic for handling requests and returning responses.
- `models.py`: Defines the data models for the application.
- `templates/`: Directory where all HTML templates are stored. 