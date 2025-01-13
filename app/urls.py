from django.urls import path
from app.views import ArticleListView, CreateArticleView, UpdateArticleView, DeleteArticleView


urlpatterns = [
    path("", ArticleListView.as_view(), name="home"),
    path("create/", CreateArticleView.as_view(), name="create_article"),
    path("<int:pk>/update",
         UpdateArticleView.as_view(), name="update_article"),
    path("<int:pk>/delete",
         DeleteArticleView.as_view(), name="delete_article"),
]
