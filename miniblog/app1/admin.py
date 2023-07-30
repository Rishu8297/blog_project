from django.contrib import admin
from app1.models import *

# Register your models here.
# admin.site.register(Post)

@admin.register(Post)

class PostModel_admin(admin.ModelAdmin):
    list_display = ['id','title']

