from django.contrib.sites.models import Site
from django.db import models
from company_profile.cp_articles.models import Article
from django.utils import timezone

from django.urls import reverse

def default_now():
    return timezone.now()

class Visitor(models.Model):
    created_date = models.DateTimeField(db_index=True,default=default_now)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE,related_name='visitor_site', null=True, blank=True)
    
class Comment(models.Model):
    created_date = models.DateTimeField(db_index=True,default=default_now)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, related_name="article_comment", on_delete=models.CASCADE)
    content = models.TextField(max_length=550,null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,related_name='comment_site', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def get_reply_url(self):
        return "%s" % (reverse('cms:reply_add', kwargs={'pk':self.pk}))

    def get_delete_url(self):
        return "%s" % (reverse('cms:comment_edit_approve_delete', kwargs={'action':'delete', 'pk':self.pk}))

    def get_approve_url(self):
        return "%s" % (reverse('cms:comment_edit_approve_delete', kwargs={'action':'approve', 'pk':self.pk}))

class Reply(models.Model):
    created_date = models.DateTimeField(db_index=True,default=default_now)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, related_name="comment_reply", on_delete=models.CASCADE)
    content = models.TextField(max_length=550,null=True)
    is_approved = models.BooleanField(default=False)


    def get_delete_url(self):
        return "%s" % (reverse('cms:reply_edit_approve_delete', kwargs={'action':'delete', 'pk':self.pk}))

    def get_approve_url(self):
        return "%s" % (reverse('cms:reply_edit_approve_delete', kwargs={'action':'approve', 'pk':self.pk}))