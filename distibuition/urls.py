from django.urls import path
from . import views

urlpatterns = [
    path('Pajina-Distribuisaun.html/', views.dash_d, name="dist-dash"),
    path('Pajina-Monitorizasaun.html/', views.dash_c, name="dist-mon"),



    path('Distribution/summary/', views.summaryDistribusi, name='summary-distribusi'),
]