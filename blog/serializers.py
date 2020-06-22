from rest_framework import serializers

from .models import Tag, Article, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    addDate = serializers.CharField(source='add_at')

    class Meta:
        model = Comment
        fields = ['author', 'content', 'addDate']


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField()
    updateDate = serializers.CharField(source='updated_at')

    class Meta:
        model = Article
        fields = ['author', 'title', 'content', 'updateDate', 'tags', 'comments']

    def get_tags(self, instance):
        tags = sorted(instance.tags.all(), key=lambda t: t.rating, reverse=True)
        return TagSerializer(tags, many=True).data

    def get_comments(self, instance):
        comments = instance.comments.all().order_by('-add_at')
        return CommentSerializer(comments, many=True).data
