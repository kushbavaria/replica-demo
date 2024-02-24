import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
django.setup()

from django.contrib.auth.models import User

username = "creation"
email = "creation@gmail.com"
password = "holofira"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created.")
else:
    print("Superuser already exists.")
