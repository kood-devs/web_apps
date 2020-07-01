from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeForm.as_view(), name='index'),
    path('scrape_app/', include('scrape_app.urls')),
    path('forecast_app/', include('forecast_app.urls')),
    path('factor_app/', include('factor_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
