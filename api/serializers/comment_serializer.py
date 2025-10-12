from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Comment, Post

class CommentAuthorSerializer(serializers.ModelSerializer):
    """Serializer for displaying minimal author info in comments"""
    is_admin = serializers.BooleanField(source='is_staff', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'is_admin']

class CommentSerializer(serializers.ModelSerializer):
    # Nested serializer for reading (GET requests)
    author = CommentAuthorSerializer(read_only=True)
    
    # Fields for writing (POST/PUT requests)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
        required=False  # Optional since it's set automatically from token
    )
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'post', 'created_at', 'updated_at']