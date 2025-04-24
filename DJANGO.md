```bash
pip install django djangorestframework
django-admin --version
python -m django --version
mkdir uiu-aide
cd uiu-aide
django-admin startproject config .
mkdir apps
cd apps
django-admin startapp test_users

## add test_users to settings.py inside INSTALLED_APPS

# for supabase 
pip install requests python-dotenv
pip install supabase
pip install httpx postgrest


# create a __init__.py file in the apps directory if it doesn't exist, which will make it a package

# add in manage.py before execute_from line
 sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))    



# run server
python manage.py migrate
# python manage.py runserver
python manage.py runserver 127.0.0.1:5000

# install all depenencies:
pip install -r requirements.txt
```