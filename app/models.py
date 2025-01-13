import re
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from app.managers import UserProfileManager

ARTICLE_STATUS = (
    ("draft", "draft"), ("inprogress", "in progress"), ("published", "published"))


class UserProfile(AbstractUser):
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    objects = UserProfileManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def article_count(self):
        return self.articles.count()

    @property
    def written_words(self):
        return self.articles.aggregate(models.Sum("word_count"))["word_count__sum"] or 0


class Article(models.Model):
    title = models.CharField(_("title"), max_length=100)
    content = models.TextField(_("content"), blank=True, default="")
    word_count = models.IntegerField(_("word count"), blank=True, default="")
    twitter_post = models.TextField(_("twitter post"), blank=True, default="")
    status = models.CharField(
        _("status"), max_length=20, choices=ARTICLE_STATUS, default="draft")
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("creator"), related_name="articles")

    def save(self, *args, **kwargs):
        text = re.sub(r"<[^>]*>", "", self.content.replace("&nbsp;", " "))
        self.word_count = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
