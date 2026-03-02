from django.urls import path
from . import views

urlpatterns = [
	path('Sumario-Geral.html/', views.summary, name="sum"),
]