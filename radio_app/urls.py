"""radio_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from register import views as register_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path to admin page - superuser only
    path('admin/', admin.site.urls),
    # home app path relative to this
    path('', include("home.urls")),
    # default paths for user login and logout
    path('', include("django.contrib.auth.urls")),
    # register view path
    path('register/', register_views.registration_view, name='register'),
    # paths in recording app relative to this
    path('recordings/', include("recordings.urls")),
    # paths in account app relative to this
    path('<slug:username>/', include("account.urls")),
]

# url pattern to static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
