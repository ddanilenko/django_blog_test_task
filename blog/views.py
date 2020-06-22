from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blog.models import Article
from blog.serializers import ArticleSerializer


@csrf_exempt
def article_list(request):
    """
    List all articles.
    """
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)


def article_detail(request, pk):
    """
    Retrieve article.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)
