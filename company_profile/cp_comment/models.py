from django.db import models
from company_profile.cp_articles.models import Article

class Visitor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="article_comment", on_delete=models.CASCADE)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name="comment_reply", on_delete=models.CASCADE)