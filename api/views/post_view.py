from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from api.models import Post
from api.serializers import PostSerializer, CommentSerializer

class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Post model has 'author' field, not 'user'
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        # Only allow the author to update their own post
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You do not have permission to update this post.')
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only allow the author to delete their own post
        if instance.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete this post.')
        instance.delete()
        
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific post
        Example: /api/posts/1/comments/
        """
        post = self.get_object()
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
