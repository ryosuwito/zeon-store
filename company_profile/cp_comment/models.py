from django.db import models
from company_profile.cp_articles.models import Article
from django.utils import timezone

class Visitor(models.Model):
    created_date = models.DateTimeField(db_index=True,default=timezone.now)
    name = models.CharField(max_length=50)
    email = models.EmailField()


class Comment(models.Model):
    created_date = models.DateTimeField(db_index=True,default=timezone.now)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, related_name="article_comment", on_delete=models.CASCADE)
    content = models.TextField(null=True)

class Reply(models.Model):
    created_date = models.DateTimeField(db_index=True,default=timezone.now)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, related_name="comment_reply", on_delete=models.CASCADE)
    content = models.TextField(null=True)