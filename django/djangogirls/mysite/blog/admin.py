rom django.contrib import admin
from .models import Post, Comment


admin.site.register(Post)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
