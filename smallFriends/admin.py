from django.contrib import admin
from .models import Generate


class GenerateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created')
    list_display_links = ('id', 'title')

admin.site.register(Generate, GenerateAdmin)
