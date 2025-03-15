import os
import subprocess


def print_logo():
    logo = """
    ==============================================================================================================
    ||  ____  _                           ____            _           _      ____                _              ||
    || |  _ \(_) __ _ _ __   __ _  ___   |  _ \ _ __ ___ (_) ___  ___| |_   / ___|_ __ ___  __ _| |_ ___  _ __  ||
    || | | | | |/ _` | '_ \ / _` |/ _ \  | |_) | '__/ _ \| |/ _ \/ __| __| | |   | '__/ _ \/ _` | __/ _ \| '__| ||
    || | |_| | | (_| | | | | (_| | (_) | |  __/| | | (_) | |  __/ (__| |_  | |___| | |  __/ (_| | || (_) | |    ||
    || |____// |\__,_|_| |_|\__, |\___/  |_|   |_|  \___// |\___|\___|\__|  \____|_|  \___|\__,_|\__\___/|_|    ||
    ||     |__/             |___/                      |__/                                                     ||
    ||                                                                                                          ||
    ||                                                                                                          ||
    ==============================================================================================================
    🚀 Django Project Creator - v1.0 🎯
    Developed by: Youssef Ahmed
    LinkedIn: www.linkedin.com/in/yousef-ahmed-40b6401b3
    WhatsApp: https://wa.me/+202091972984
    ========================================
    """
    print(logo)
    print("\nDescription: This script automates the setup of a Django project with a miner theme!\n")
    print("Usage Instructions:")
    print("1. Enter the project name when prompted.")
    print("2. Choose the project location (Desktop or Custom).")
    print("3. Choose applications to create (optional).")
    print("4. Select libraries to install from the list.")
    print("5. Wait for the setup to complete and follow instructions to create a superuser.\n")

def get_user_input():
    project_name = input("Enter project name (required): ").strip().capitalize().replace(' ', '_')
    while not project_name:
        print("Project name cannot be empty.")
        project_name = input("Enter project name (required): ").strip().capitalize().replace(' ', '_')

    location_choice = input("Choose project location: (1) Desktop (2) Custom: ")
    while not location_choice or location_choice not in ["1", "2"]:
        print("Invalid choice. Enter 1 for Desktop or 2 for Custom.")
        location_choice = input("Choose project location: (1) Desktop (2) Custom: ")

    if location_choice == "1":
        project_location = os.path.expanduser("~\Desktop")
    else:
        project_location = input("Enter the full custom path: ").strip()
        while not os.path.exists(project_location):
            print("Invalid path. Please enter an existing directory.")
            project_location = input("Enter the full custom path: ").strip()

    apps = input("Enter application names (optional, separate by commas, or type 'skip'): ")
    app_list = []
    if apps.lower() != 'skip':
        app_list = [app.strip().capitalize().replace(' ', '_') for app in apps.split(',') if app.strip()]

    common_libraries = {
        "pillow": "Image processing library for handling images in Django. (Personal Website)",
        "django": "The main Django framework. (Personal Website)",
        "djangorestframework": "Toolkit for building Web APIs in Django.",
        "django-rest-knox": "Token-based authentication for Django REST Framework.",
        "django-rest-passwordreset": "Password reset via Django REST Framework.",
        "requests": "HTTP library for making API requests.",
        "apscheduler": "Task scheduling for Django applications.",
        "firebase_admin": "Integration with Firebase services.",
        "django-jazzmin": "Customizable admin interface for Django.",
        "sib_api_v3_sdk": "SendinBlue API SDK for email marketing.",
        "django-ckeditor": "Rich text editor for Django models. (Personal Website)",
        "channels": "WebSockets support for Django.",
        "moviepy": "Video editing library useful for Django apps.",
        "django-robots-txt": "Manage robots.txt files for SEO.",
        "django-allauth": "User authentication and social login integration. (Personal Website)",
        "django-admin-logs": "Logging system for Django admin.",
        "reportlab": "PDF generation in Django.",
        "pdfkit": "Convert HTML to PDFs in Django applications.",
        "channels_redis": "Redis support for Django Channels.",
        "django-admin-charts": "Admin panel data visualization.",
        "django-light": "Lightweight Django utilities and enhancements.",
        "django-crispy-forms": "Enhanced form rendering with Bootstrap support. (Personal Website)",
        "django-haystack": "Search functionality integration for Django.",
        "django-storages": "Storage backend support for cloud services.",
        "whitenoise": "Serve static files efficiently."
    }

    print("\nSelect libraries to install:")
    for i, (lib, desc) in enumerate(common_libraries.items(), 1):
        print(f"{i}. {lib} - {desc}")

    selected_libs = input("Enter numbers separated by commas or type extra libraries: ")
    print("Waiting for the project creation...")
    selected_libs_list = []

    if selected_libs:
        selected_libs_list = [list(common_libraries.keys())[int(i)-1] for i in selected_libs.split(',') if i.strip().isdigit() and 1 <= int(i) <= len(common_libraries)]
        extra_libs = [lib.strip() for lib in selected_libs.split(',') if not lib.strip().isdigit()]
        selected_libs_list.extend(extra_libs)

    return project_name, project_location, app_list, selected_libs_list


def execute_command(cmd):
    subprocess.run(cmd, shell=True, check=True)


def execute_in_session(commands):
    process = subprocess.Popen("cmd", stdin=subprocess.PIPE, text=True)
    for cmd in commands:
        process.stdin.write(cmd + "\n")
    process.stdin.close()
    process.wait()


def create_django_project(project_name, project_location, app_list, selected_libs_list):
    project_path = os.path.join(project_location, project_name)

    os.chdir(project_location)
    execute_command(f"virtualenv {project_name}")

    activate_script = os.path.join(project_path)
    if not os.path.exists(activate_script):
        print("Error: Virtual environment activation script not found.")
        exit(1)

    session_commands = [
        f"cd {activate_script}",
        ".\scripts\\activate",
        "pip freeze"
    ]

    for lib in selected_libs_list:
        session_commands.append(f"pip install {lib}")

    session_commands.append("pip freeze")


    src_path = os.path.join(project_path, "src")
    os.makedirs(src_path, exist_ok=True)
    execute_command(f"cd {src_path} && django-admin startproject {project_name}")

    project_src_path = os.path.join(src_path, project_name)

    session_commands.append(f"cd {project_src_path} && pip freeze > req.txt")
    execute_in_session(session_commands)

    execute_command(f"cd {project_src_path}")

    for app in app_list:
        execute_command(f"cd {project_src_path} && django-admin startapp {app}")

    execute_command(f"cd {project_src_path} && python manage.py makemigrations")
    execute_command(f"cd {project_src_path} && python manage.py migrate")

    print("\nCreating superuser manually. Please enter details when prompted.")
    execute_command(f"cd {project_src_path} && python manage.py createsuperuser")

    print("\nSetup completed. Runing 'python manage.py runserver' to start the project.")
    execute_command(f"cd {project_src_path} && python manage.py runserver")


if __name__ == "__main__":
    print_logo()
    project_name, project_location, app_list, selected_libs_list = get_user_input()
    create_django_project(project_name, project_location, app_list, selected_libs_list)
