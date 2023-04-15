from .models import Article
from django.views.generic import ListView


class ArticleListView(ListView):
    model = Article
    context_object_name = "article_list"
    template_name = "home.html"
