from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from NoteApp import urls, views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include(urls)),
]