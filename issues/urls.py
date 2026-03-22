from django.contrib import admin
from django.urls import path

from .views import IssuesView

urlpatterns = [
    path('issues/', IssuesView.as_view()),
]