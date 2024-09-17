from django.urls import path
from .views import UploadFeed

from django.contrib import admin
from django.urls import path, include
from content.views import Main, UploadFeed


urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('main', Main.as_view())
]