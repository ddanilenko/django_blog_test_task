from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=200, validators=[MinLengthValidator(5)])
    slug = models.CharField(unique=True, max_length=200)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def rating(self):
        return self.article_set.count()


class Article(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(unique=True, max_length=200, validators=[MinLengthValidator(5)])
    content = models.CharField(max_length=1000)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comments(self):
        return self.comment_set.all()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Article, self).save(*args, **kwargs)

    @staticmethod
    def comment_statistics():
        articles = Article.objects.filter(tags__isnull=False)
        stats = {article.title: len(article.comment_set.all()) for article in articles}
        return stats


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    add_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-add_at']

    def __str__(self):
        return self.content[:30] + "..."

    @property
    def is_article_author(self):
        return self.author == self.article.author
