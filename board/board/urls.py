import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from board import settings

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),

    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),

    path('', include('custom_user.urls')),
    path('mysite/', include('mysite.urls')),

    path('api/', include('custom_user.api.urls')),
    path('mysite/api/', include('mysite.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
