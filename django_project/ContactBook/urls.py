"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from ContactBook import views
from django.conf.urls.static import static
from django.conf import settings
from .views import Contacts, delete_contact, edit_contact, SearchContact

urlpatterns = [
    path('', Contacts, name = 'contacts_list'),
    path('delete_contact/<int:contact_id>/',delete_contact, name = "delete_contact"),
    path('edit_contact/<int:contact_id>/',edit_contact),
    path('search',SearchContact, name="search_contact"),
]