from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (PostView, CommentView, CategoryView)
from api.views.auth_view import RegisterView, login_view, logout_view, profile_view
router = DefaultRouter()
router.register(r'posts', PostView, basename='post')    
router.register(r'comments', CommentView, basename='comment')
router.register(r'categories', CategoryView, basename='category')
urlpatterns = [
    path('', include(router.urls)),

    # auth urls
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', profile_view, name='profile'),
]