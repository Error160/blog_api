# Blog API - Django REST Framework

A complete blog/social media API built with Django REST Framework featuring posts, comments, categories, and user authentication.

## 🚀 Features

- **User Authentication** (Token-based)
  - Register, Login, Logout
  - User profiles with admin status
- **Posts Management**
  - Create, Read, Update, Delete posts
  - Only authors can modify their posts
  - Nested author and category info
- **Comments System**
  - Comment on posts
  - Only authors can modify their comments
- **Categories** (Admin-only management)
  - Public read access
  - Admin-only create/update/delete
- **Security**
  - Token authentication
  - Owner-based permissions
  - Admin role checking

## 📋 Requirements

- Python 3.10+
- Django 5.2.7
- Django REST Framework 3.16.1
- See `requirements.txt` for full dependencies

## 🛠️ Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd dummy_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit: `http://localhost:8000/api/`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout (requires token)
- `GET /api/auth/profile/` - Get current user from token

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create post (authenticated)
- `GET /api/posts/{id}/` - Get single post
- `PUT/PATCH /api/posts/{id}/` - Update post (author only)
- `DELETE /api/posts/{id}/` - Delete post (author only)
- `GET /api/posts/{id}/comments/` - Get post comments

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create comment (authenticated)
- `GET /api/comments/{id}/` - Get single comment
- `PUT/PATCH /api/comments/{id}/` - Update comment (author only)
- `DELETE /api/comments/{id}/` - Delete comment (author only)

### Categories
- `GET /api/categories/` - List all categories (public)
- `POST /api/categories/` - Create category (admin only)
- `GET /api/categories/{id}/` - Get single category
- `PUT/PATCH /api/categories/{id}/` - Update category (admin only)
- `DELETE /api/categories/{id}/` - Delete category (admin only)

## 🌐 Deployment

### PythonAnywhere
See **[PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)** for detailed deployment instructions.

Quick WSGI file for PythonAnywhere - see `pythonanywhere_wsgi.py`

### Other Platforms
- Render: Use `build.sh` for build commands
- Heroku: Add `Procfile` with gunicorn
- DigitalOcean/AWS: Configure nginx + gunicorn

## 🔐 Authentication

All authenticated requests require a token in the header:

```
Authorization: Token <your-token-here>
```

Get token from login endpoint:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

## 📝 Example Usage

```javascript
// Login
const response = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'password123' })
});
const { token, user } = await response.json();

// Create Post
const postResponse = await fetch('/api/posts/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'My Post',
    category_id: 1,
    content: 'Post content...'
  })
});
```

## 🔑 Admin Access

Create admin user:
```bash
python manage.py createsuperuser
```

Admin panel: `http://localhost:8000/admin/`

## 📄 License

MIT License

## 👤 Author

Your Name
