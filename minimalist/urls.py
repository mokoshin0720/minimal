from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from minimal import views

handler500 = views.my_customized_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('minimal.urls')),
    path('', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
 + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIR)