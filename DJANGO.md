
# Django REST API Project Setup with Supabase PostgreSQL

This guide outlines how to set up a Django REST API project using the MVC pattern, with Supabase PostgreSQL as the database.

---

## Prerequisites

- Python 3.8+
- pip
- [Supabase account](https://supabase.com/)
- PostgreSQL connection details from Supabase

---

## 1. Create Supabase Project & Get DB Credentials

1. Sign in to [Supabase](https://app.supabase.com/).
2. Create a new project.
3. Go to **Project Settings > Database** to find:
    - Host
    - Port
    - Database name
    - User
    - Password

---

## 2. Set Up Django Project

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django djangorestframework psycopg2-binary python-dotenv
django-admin startproject myproject
cd myproject
python manage.py startapp api
```

---

## 3. Configure Database with Environment Variables (MVC: Model)

**Create a `.env` file in your project root:**

```env
DB_NAME=<supabase_db_name>
DB_USER=<supabase_user>
DB_PASSWORD=<supabase_password>
DB_HOST=<supabase_host>
DB_PORT=5432
```

**Edit `myproject/settings.py`:**

Add at the top:

```python
import os
from dotenv import load_dotenv
load_dotenv()
```

Update the `DATABASES` setting:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

**Add `.env` to your `.gitignore` to keep credentials safe:**

```
.env
```

---

## 4. Register App & REST Framework

In `myproject/settings.py`:

```python
INSTALLED_APPS = [
     # ...
     'rest_framework',
     'api',
]
```

---

## 5. Create a Model (MVC: Model)

In `api/models.py`:

```python
from django.db import models

class Item(models.Model):
     name = models.CharField(max_length=100)
     description = models.TextField()
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Create a Serializer (MVC: View)

In `api/serializers.py`:

```python
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
     class Meta:
          model = Item
          fields = '__all__'
```

---

## 7. Create API Views (MVC: Controller)

In `api/views.py`:

```python
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
     queryset = Item.objects.all()
     serializer_class = ItemSerializer
```

---

## 8. Set Up URLs

In `api/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
     path('', include(router.urls)),
]
```

In `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/', include('api.urls')),
]
```

---

## 9. Test the API

Run the server:

```bash
python manage.py runserver
```

Visit `http://localhost:8000/api/items/` to interact with your REST API.

---

## Notes

- Use Django admin to manage data: `python manage.py createsuperuser`
- Store credentials in `.env` and never commit it to version control
- Use `python-dotenv` to load environment variables in development
- Supabase PostgreSQL acts as your remote DB; all Django ORM queries interact with it

