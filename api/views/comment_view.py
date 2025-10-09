from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import Comment
from api.serializers import CommentSerializer

class CommentView(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter comments by post
        Example: /api/comments/?post=1
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        
        return queryset

    def perform_create(self, serializer):
        # Comment model has 'author' field, not 'user'
        serializer.save(author=self.request.user)
