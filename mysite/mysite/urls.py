from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace='accounts')),  # Primeiro importa o app personalizado
    path('accounts/', include('django.contrib.auth.urls')),  # Depois adiciona as URLs do Django Auth
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
