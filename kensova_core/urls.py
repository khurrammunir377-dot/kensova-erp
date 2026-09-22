from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store_app.urls')),
    # DEBUG is False, so Django's normal auto-static-serving is off. This app
    # runs via `manage.py runserver` directly (no separate web server in
    # front of it), so it needs to serve its own static files this way.
    re_path(r'^static/(?P<path>.*)$', static_serve, {'document_root': settings.STATIC_ROOT}),
]