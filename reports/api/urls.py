from django.urls import path
from . import views_api

urlpatterns = [
    path('dist/gab/', views_api.APIDistGab.as_view()),

]