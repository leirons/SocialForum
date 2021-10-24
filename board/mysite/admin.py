from django.contrib import admin
from .models import *

from preferences.admin import PreferencesAdmin
from .preferences import MyPreference


class ThemeDisplay(admin.ModelAdmin):
    list_display = ('title', 'subject', 'slug')
    list_editable = ['slug', ]
    prepopulated_fields = {'slug': ('title',), }


class SubjectsDisplay(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Subject, SubjectsDisplay)
admin.site.register(Theme, ThemeDisplay)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(StoorageLikes)


admin.site.register(MyPreference, PreferencesAdmin)