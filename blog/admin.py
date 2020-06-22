from django.contrib import admin

from blog.models import Article, Comment
from .models import Tag


class RatingFilter(admin.SimpleListFilter):
    title = 'Rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        ratings = set([tag.rating for tag in model_admin.get_queryset(request)])
        return [(str(rating), rating) for rating in ratings]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        tag_ids = [tag.id for tag in queryset if str(tag.rating) == self.value()]
        return queryset.filter(id__in=tag_ids)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'rating')
    fields = ('title', 'slug', 'rating')
    list_filter = (RatingFilter,)
    search_fields = ('title', 'slug')
    readonly_fields = ('rating',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'content', 'is_article_author')
    fields = ('author', 'article', 'content', 'is_article_author')
    search_fields = ('author', 'article', 'is_article_author')
    readonly_fields = ('is_article_author',)


admin.site.register(Article)
