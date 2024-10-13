from django.contrib import admin
from .models import Generate, Telegram


class GenerateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created')
    list_display_links = ('id', 'title')

admin.site.register(Generate, GenerateAdmin)
@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chat_id')
    list_display_links = ('id', 'user')
    list_editable = ('chat_id', )
