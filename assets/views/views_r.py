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


# views los ba rir 
@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def List_rir(request):
    group = request.user.groups.values_list('name', flat=True).first()
    objects = RIR.active_objects.select_related().all()
    context = {
        'group': group,
        'page': 'rir',
        'objects': objects,
        'title': 'Lista Lista Rir',
        'legend': 'Lista Lista Rir',
        'RirActive': "active",
        'link_antes': [{'link_name':"r-list",'link_text':"Rir"}],
    }
    return render(request, 'Rir/list_r.html', context)

@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def add_rir(request):
    if request.method == "POST":
        form = RIRForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            newid = getjustnewid(RIR)
            instance.hashed = hash_md5(str(newid))
            instance.created_by = request.user
            instance.save()

            messages.success(request, "RIR kria ho susesu! Agora aumenta item Rir.")
            return redirect("rir_item_create", rir_id=instance.id)
    else:
        form = RIRForm()

    context = {
        'form': form,
        'title': "Rejistu RIR",
        'legend': "Formulario Rejistu RIR",
    }
    return render(request, "Rir/rir_form.html", context)


@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def rir_item_create(request, hashed):
    rir = get_object_or_404(RIR, hashed=hashed)

    if request.method == "POST":
        form = RIRItemForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            newid = getjustnewid(RIRItem)
            instance.hashed = hash_md5(str(newid))
            instance.rir = rir
            instance.created_by = request.user
            instance.save()

            messages.success(request, f"Item {instance.category.name} Sesuso Adisiona ona Ba Rir{rir.rir_no}")
            return redirect("rir_item_create", hashed=rir.hashed) 
    else:
        form = RIRItemForm()

    context = {
        'form': form,
        'rir': rir,
        'title': f"Resjitu item RIR {rir.rir_no}",
        'legend': "Formulario Rejistu item RIR",
    }
    return render(request, "Rir/rir_form.html", context)


@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def import_rir_excel(request):
    if request.method == "POST" and request.FILES.get("file"):
        excel_file = request.FILES["file"]
        df = pd.read_excel(excel_file)
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
        df = df.fillna("")
        request.session["excel_data"] = df.to_dict(orient="records")
        return JsonResponse({
            "status": "success",
            "data": request.session["excel_data"]
        })
    return JsonResponse({"status": "error"})

@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def save_import_rir(request):
    if request.method == "POST":
        selected_rows = json.loads(request.POST.get("selected_rows"))
        for row in selected_rows:
            rir, created = RIR.objects.get_or_create(
                rir_no=row["rir_no"],
                defaults={
                    "invoice_no": row.get("invoice_no", ""),
                    "container_no": row.get("container_no", ""),
                    "company_id": row.get("company_id"),
                    "arrival_date": row.get("arrival_date"),
                    "created_by": request.user,
                    "hashed": hash_md5(str(getjustnewid(RIR)))
                }
            )

            category = Category.objects.filter(
                name=row.get("category")
            ).first()

            brand = Brand.objects.filter(
                name=row.get("brand")
            ).first()

            model = Model.objects.filter(
                name=row.get("model")
            ).first()

            if not category or not brand or not model:
                continue

            RIRItem.objects.create(
                rir=rir,
                category=category,
                brand=brand,
                model=model,
                purchase_type=row.get("purchase_type"),
                quantity=row.get("quantity", 0),
                unit_cost=row.get("unit_cost", 0),
                created_by=request.user,
                hashed=hash_md5(str(getjustnewid(RIRItem)))
            )

        return JsonResponse({"status": "saved"})


@login_required
@allowed_users(allowed_roles=['Admin_Asset'])
def rir_approve(request, hashed):
    rir = get_object_or_404(RIR, hashed=hashed)
    if not rir.is_approved:
        rir.is_approved = True
        rir.save()
        try:
            with transaction.atomic():
                for item in rir.items.all():
                    for i in range(item.quantity):
                        Equipment.objects.create(
                            rir_item=item,
                            barcode=generate_barcode(),
                            serial_no="",  
                            status=Status.objects.get(name="In Stock"),
                            location=Location.objects.get(id=1),  
                            purchase_year=rir.arrival_date.year,
                            cost=item.unit_cost if item.purchase_type == "Sosa" else 0,
                            created_by=request.user
                        )
        except Exception as e:
            messages.error(request, f"Error generate equipment: {str(e)}")
            return redirect("r-list")
        messages.success(request, "RIR Approved & Equipment Generated Successfully!")
    return redirect("r-list")


@login_required
@allowed_users(allowed_roles=['Admin_Asset', 'Staffassets'])
def detail_rir(request, hashed):
    group = request.user.groups.values_list('name', flat=True).first()
    objects = get_object_or_404(RIR, hashed=hashed)
    objects1 = RIRItem.active_objects.filter(rir=objects)
    context = {
        'group': group,
        'page': 'rir_detl',
        'objects': objects,
        'title': f'Detaillu Dadus Rir {objects.rir_no}',
        'legend': f'Detaillu Dadus Rir {objects.rir_no}',
        'RirActive': "active",
        'link_antes': [{'link_name':"r-list",'link_text':"Rir"}],
    }
    return render(request, 'Rir/list_dtl.html', context)