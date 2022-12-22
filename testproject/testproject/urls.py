"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.admin import AdminSite
from django.urls import path
from django.http import HttpResponse


def custom_password_change(request):
    return HttpResponse('OK')

autai_site = AdminSite(name='autai')

urlpatterns = [
    path('custom_password_change/', custom_password_change, name='custom_password_change')
    path('admin/', admin.site.urls),
    path('autai/', autai_site.urls),
]
