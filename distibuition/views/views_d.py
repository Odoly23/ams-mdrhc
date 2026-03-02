import csv, io, datetime
from django.shortcuts import render, get_object_or_404
from main.utils import getjustnewid
from django.contrib.auth.decorators import login_required
from config.decorators import allowed_users

# Create your views here.
@login_required
def dash_d(request):
	context = {
		'link_antes': [{'link_name':"dist-dash",'link_text':"Dados Distribuisaun"}],
		'title': 'Sumario Distribuisaun Assets',
		'legend': 'Sumario Distribuisaun Assets',
		'distActive':"active",
	}
	return render(request, 'Dash/index_d.html', context)


@login_required
def dash_c(request):
	context = {
		'link_antes': [{'link_name':"dist-dash",'link_text':"Dados Inventorio"}],
		'title': 'Lista Ekipamento Inventorio',
		'legend': 'Lista Ekipamento Inventorio',
		'intActive':"active",
	}
	return render(request, 'Monitoring/monit.html', context)


@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def detl_dist(request):
	group = request.user.groups.all()[0].name
	objects = Distribuition.active_objects.select_related.all()
	context:{
		'link_antes':[{'link_name':'d-list', 'link_text':"Dados Inventorio"}],
		'title':'Detaillo Dados Distribuisaun',
		'legend': 'Detaillo Dados Distribuisaun',
		'objects': 'objects',
		'group':group
	}
	return render(render, 'Monitoring/detl_moni.html', context)