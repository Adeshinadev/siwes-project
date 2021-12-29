"""efc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.urls import path

urlpatterns = [

    path('', views.home, name='home'),
    path('upload_details', views.upload_details, name='upload_details'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('Login', views.Login, name='Login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('export_excel/', views.export_excel, name='export_excel'),
]
