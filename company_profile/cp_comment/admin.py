from django.contrib import admin
from .models import Comment, Reply, Visitor

class CommentAdmin(admin.ModelAdmin):
    model = Comment

class ReplyAdmin(admin.ModelAdmin):
    model = Reply

class VisitorAdmin(admin.ModelAdmin):
    model = Visitor

admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Visitor, VisitorAdmin)