from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post
from api.models.category import Category

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for displaying minimal author info in posts"""
    is_admin = serializers.BooleanField(source='is_staff', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'is_admin']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class PostSerializer(serializers.ModelSerializer):
    # Nested serializers for reading (GET requests)
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    # Fields for writing (POST/PUT requests)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
        required=False  # Optional since it's set automatically from token in view
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_id', 'category', 'category_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']