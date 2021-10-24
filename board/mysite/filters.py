import django_filters

from .models import *

class Filter(django_filters.FilterSet):
    class Meta:
        model = Theme
        fields = ['title']
