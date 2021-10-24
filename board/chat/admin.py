from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

from .models import Chat, ChatMessage
# Register your models here.


class Chat(admin.ModelAdmin):
    list_display = ['id','title']