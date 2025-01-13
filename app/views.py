
from django.http import HttpResponse
from app.models import Article
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ArticleListView(LoginRequiredMixin, ListView):
    template_name = "app/home.html"
    model = Article
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user).order_by("-created_at")


class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "app/article_create.html"
    model = Article
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "app/article_update.html"
    model = Article
    fields = ["title", "status", "content", "twitter_post"]
    context_object_name = "article"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.request.user == self.get_object().creator


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "app/article_delete.html"
    model = Article
    context_object_name = "article"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.request.user == self.get_object().creator
