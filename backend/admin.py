from django.contrib import admin

# Register your models here.
from backend.models import Post


@admin.register(Post)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title')