from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include('backend.urls')),
    path('api/', include('backend.api.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]