from django.urls import path
from . import views

urlpatterns = [
	path('Lista-Rir.html/', views.List_rir, name="r-list"),
	path('Rejistu-RIR.html/', views.add_rir, name='a-rir'),
	path('Rejistu-ITEM-RIR/<str:hashed>/.html', views.rir_item_create, name='rir_item_create'),
	path('Upload-excel/', views.import_rir_excel, name='import_rir_excel'),
	path('Save-import/', views.save_import_rir, name='save_import_rir'),
	path('aprova-rir/<str:hashed>/', views.rir_approve, name='aprova-rir'),
	path('Detaillu-dadus-rir/<str:hashed>/', views.detail_rir, name='d-drir'),


	#history data
	path('Lista-historia.html/', views.history_rir, name='h-rir'),


	#equipamento-gabinete
	path('Lista-Equipamento-Gabinete.html/', views.list_e_gab, name='list-gab'),
]