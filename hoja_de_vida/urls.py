from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <--- AÑADE ESTO
from django.conf.urls.static import static # <--- AÑADE ESTO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('curriculum.urls')),
]

# ESTO ES LO QUE FALTA PARA QUE LA IMAGEN SE MUESTRE:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)