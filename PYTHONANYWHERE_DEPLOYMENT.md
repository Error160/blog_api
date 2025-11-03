# PythonAnywhere Deployment Guide

## 📋 Prerequisites
- PythonAnywhere account (Free or Paid)
- Your project code ready to deploy

---

## 🚀 Step-by-Step Deployment

### 1. **Upload Your Project to PythonAnywhere**

#### Option A: Using Git (Recommended)
```bash
# On PythonAnywhere Bash Console
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git dummy_api
cd dummy_api
```

#### Option B: Upload Files Manually
- Use the "Files" tab in PythonAnywhere
- Create a directory: `/home/YOUR_USERNAME/dummy_api`
- Upload all your project files

---

### 2. **Set Up Virtual Environment**

```bash
# On PythonAnywhere Bash Console
cd ~/dummy_api

# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. **Update Settings for Production**

Edit `config/settings.py` on PythonAnywhere:

```python
# Add your PythonAnywhere domain to ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'YOUR_USERNAME.pythonanywhere.com',  # ⚠️ CHANGE THIS
]

# For production, set DEBUG to False (after testing)
DEBUG = False  # Change this after confirming everything works

# Database - Use MySQL for production (optional)
# Or keep SQLite for testing:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

---

### 4. **Run Migrations and Collect Static Files**

```bash
# On PythonAnywhere Bash Console
cd ~/dummy_api
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

### 5. **Configure Web App in PythonAnywhere**

1. Go to the **Web** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (not Django wizard)
4. Select **Python 3.10** (or your preferred version)

---

### 6. **Configure WSGI File**

In the **Web** tab, click on the **WSGI configuration file** link.

**Replace ALL content** with this:

```python
# +++++++++++ DJANGO +++++++++++
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/dummy_api'  # ⚠️ CHANGE YOUR_USERNAME
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Activate your virtual environment
virtualenv_path = '/home/YOUR_USERNAME/dummy_api/venv'  # ⚠️ CHANGE YOUR_USERNAME
activate_this = os.path.join(virtualenv_path, 'bin/activate_this.py')

# For Python 3.x
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANT:** Replace `YOUR_USERNAME` with your actual PythonAnywhere username!

---

### 7. **Configure Static Files**

In the **Web** tab, scroll to **Static files** section:

Add these entries:

| URL           | Directory                                        |
|---------------|--------------------------------------------------|
| `/static/`    | `/home/YOUR_USERNAME/dummy_api/staticfiles`     |

---

### 8. **Configure Virtual Environment Path**

In the **Web** tab, under **Virtualenv** section:

```
/home/YOUR_USERNAME/dummy_api/venv
```

---

### 9. **Reload Your Web App**

Click the green **"Reload"** button at the top of the Web tab.

---

### 10. **Test Your API**

Visit your API at:
```
https://YOUR_USERNAME.pythonanywhere.com/api/posts/
https://YOUR_USERNAME.pythonanywhere.com/api/auth/login/
https://YOUR_USERNAME.pythonanywhere.com/admin/
```

---

## 🔧 Troubleshooting

### Check Error Logs
In the **Web** tab:
- **Error log** - Shows Python errors
- **Server log** - Shows HTTP requests

### Common Issues:

#### 1. **Import Error / Module Not Found**
```bash
# Reinstall packages
cd ~/dummy_api
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. **Static Files Not Loading**
```bash
python manage.py collectstatic --noinput
```
Then check Static files configuration in Web tab.

#### 3. **Database Errors**
```bash
python manage.py migrate
```

#### 4. **Permission Denied**
```bash
chmod -R 755 ~/dummy_api
```

---

## 🔐 Security Checklist

Before going to production:

1. ✅ Set `DEBUG = False` in settings.py
2. ✅ Set a strong `SECRET_KEY` (use environment variable)
3. ✅ Configure proper `ALLOWED_HOSTS`
4. ✅ Use HTTPS (PythonAnywhere provides this automatically)
5. ✅ Change admin password to something strong
6. ✅ Review CORS settings if using frontend

---

## 📝 Environment Variables (Optional)

For better security, use environment variables:

1. Create a `.env` file (don't commit to git):
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
```

2. Install python-decouple:
```bash
pip install python-decouple
```

3. Update settings.py:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
```

---

## 🔄 Updating Your App

When you make changes:

```bash
# Pull latest code (if using git)
cd ~/dummy_api
git pull

# Activate venv
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations (if any)
python manage.py migrate

# Collect static files (if changed)
python manage.py collectstatic --noinput

# Reload the web app (or use Web tab button)
touch /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
```

Or just click **Reload** in the Web tab!

---

## 📊 Database Options

### Option 1: SQLite (Current - Good for testing)
- Easy setup
- Already configured
- Limited concurrent users

### Option 2: MySQL (Recommended for production)

1. Create MySQL database in PythonAnywhere Databases tab
2. Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'YOUR_USERNAME$dbname',
        'USER': 'YOUR_USERNAME',
        'PASSWORD': 'your-db-password',
        'HOST': 'YOUR_USERNAME.mysql.pythonanywhere-services.com',
    }
}
```

3. Install MySQL client:
```bash
pip install mysqlclient
```

4. Run migrations:
```bash
python manage.py migrate
```

---

## 🌐 Testing Your Deployed API

### Using cURL:
```bash
# Test login
curl -X POST https://YOUR_USERNAME.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'

# Test posts
curl https://YOUR_USERNAME.pythonanywhere.com/api/posts/

# Test authenticated request
curl https://YOUR_USERNAME.pythonanywhere.com/api/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Using Postman or Frontend:
Update your API base URL to:
```
https://YOUR_USERNAME.pythonanywhere.com/api/
```

---

## ✅ Quick Checklist

- [ ] Code uploaded to PythonAnywhere
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] settings.py updated with correct ALLOWED_HOSTS
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] WSGI file configured with correct paths
- [ ] Virtual environment path set in Web tab
- [ ] Static files path configured in Web tab
- [ ] Web app reloaded
- [ ] API endpoints tested and working
- [ ] Admin panel accessible

---

## 🎉 Your API Should Now Be Live!

**API Base URL:**
```
https://YOUR_USERNAME.pythonanywhere.com/api/
```

**Admin Panel:**
```
https://YOUR_USERNAME.pythonanywhere.com/admin/
```

**Endpoints:**
- `/api/auth/register/` - User registration
- `/api/auth/login/` - User login
- `/api/auth/logout/` - User logout
- `/api/auth/profile/` - Get current user
- `/api/posts/` - Posts CRUD
- `/api/comments/` - Comments CRUD
- `/api/categories/` - Categories (admin only for CUD)

---

## 📞 Need Help?

- Check PythonAnywhere forums: https://www.pythonanywhere.com/forums/
- Django deployment docs: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Your error logs in the Web tab

Good luck with your deployment! 🚀


