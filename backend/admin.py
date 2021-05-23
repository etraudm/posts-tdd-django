from django.contrib import admin

# Register your models here.
from backend.models import Post, PostComments


@admin.register(Post)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title')


@admin.register(PostComments)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'body')
