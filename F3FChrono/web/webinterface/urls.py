"""webinterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include,path
import os

public_only = os.getenv('PUBLIC_ONLY', 'False').lower() in ('true', '1', 't')
private_only = os.getenv('PRIVATE_ONLY', 'False').lower() in ('true', '1', 't')

print('public_only={}'.format(public_only))
print('private_only={}'.format(private_only))

urlpatterns = []

if not private_only :
    urlpatterns += [
        path('f3franking/', include('F3FChrono.web.f3franking.urls'))
    ]

if not public_only :
    urlpatterns += [
        path('administrator/', include('F3FChrono.web.administrator.urls')),
        path('admin/', admin.site.urls),
    ]
