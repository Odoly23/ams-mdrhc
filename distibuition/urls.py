from django.urls import path
from . import views

urlpatterns = [
    path('Pajina-Distribuisaun.html/', views.dash_d, name="dist-dash"),
    path('Pajina-Monitorizasaun.html/', views.dash_c, name="dist-mon"),



    path('report/summary/', views.summaryDistribusi, name='summary-distribusi'),
    path('report/summary/gabinete/<int:gabinete_id>/', views.detailSubGabinete, name='detail-sub-gabinete'),
    path('report/summary/diresaun/<int:diresaun_id>/', views.detailDiresaun, name='detail-diresaun'),
    path('report/summary/departamento/<int:departamento_id>/', views.detailSubDepartamento, name='detail-sub-departamento'),
]