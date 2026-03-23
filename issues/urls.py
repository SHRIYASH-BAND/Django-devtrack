from django.contrib import admin
from django.urls import path

from .views import IssuesView, ReportersView

urlpatterns = [
    path('issues/', IssuesView.as_view()),
    path('reporters/', ReportersView.as_view())
]