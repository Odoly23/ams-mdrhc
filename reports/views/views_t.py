import csv, io, datetime, json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from config.decorators import allowed_users
from costum.models import BaseModel, Company, Category, Brand, Model, Source, Status, Location
from assets.models import RIR, RIRItem, Equipment
from assets.forms import RIRForm, RIRItemForm
from main.utils import generate_barcode, getjustnewid, hash_md5
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# Create your views here.
@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def summary(request):
    objects1, objects2, objects3, objects4, objects5 = [],[],[],[],[]
    group = request.user.groups.values_list('name', flat=True).first()
    context = {
        'group': group,
        'title': 'Sumario Geral',
        'legend': 'Sumario Geral',
        'sumActive': "active",
        'link_antes': [{'link_name':"r-list",'link_text':"Rir"}],

    }
    return render(request, 'sumario/tab.html', context)
    