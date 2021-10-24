from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Country, IgnoreUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'country', 'is_blocked')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'country', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_blocked',
                       'is_superuser', 'groups', 'user_permissions', 'subscribers'
                       ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_editable = ('is_blocked',)


@admin.register(IgnoreUser)
class IgnoreUserAdmin(ModelAdmin):
    list_display = ('user', 'ignored_user', 'ignore')
    search_fields = ('user__username',)


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ('name','picture', )
    search_fields = ('name',)
    list_per_page = 30

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.picture.url}>')

    def get_search_results(self, request, queryset, search_term):
        """
        Поиск в нижнем регистре
        """
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        try:
            search_term_lower = search_term.title()
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(name=search_term_lower)
        return queryset, may_have_duplicates

    get_image.short_description = 'Флаг'
