import csv, io, datetime, json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from config.decorators import allowed_users
from costum.models import BaseModel, Company, Category, Brand, Model, Source, Status, Location, \
						 Gabinete, SubGabinete, Diresaun
from assets.models import RIR, RIRItem, Equipment
from assets.forms import RIRForm, RIRItemForm
from main.utils import generate_barcode, getjustnewid, hash_md5
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from users.auth_utils import c_user_staff
from distibuition.models import Distribution

#lista Equipamento ba cada gabinete
@login_required
@allowed_users(allowed_roles=['Gabinete'])
def list_e_gab(request):
    group = request.user.groups.values_list('name', flat=True).first()
    e = c_user_staff(request.user)
    obj = e.sub_gabinete.name
    objects = Distribution.active_objects.select_related().filter(sub_gabinete=obj.name).all()
    context = {
    	'title': f'Lista Equipamento Iha Gabinete {obj.name}'
    }
    return render(request, 'Equipment/list.html', context)

