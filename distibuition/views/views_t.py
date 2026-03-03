from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from costum.models import Gabinete, SubGabinete, Diresaun, Departamento, SubDepartamento
from distibuition.models import Distribution
from django.db.models import Count, Q
from config.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['Super Admin', 'Admin_Asset', 'Staffassets'])
def summaryDistribusi(request):
    group = request.user.groups.values_list('name', flat=True).first()
    type_filter = request.GET.get("type")
    if not type_filter:type_filter = "gabinete"
    data = []
    if type_filter == "gabinete":
        items = Gabinete.objects.all()
        for item in items:
            dist = Distribution.objects.filter(sub_gabinete__gabinete=item)
            data.append({"name": item.name,"total": dist.count(),"existe": dist.filter(is_return=False).count(),"diak": dist.filter(kodition_return__name="Diak").count(),
                "aat": dist.filter(kodition_return__name="A'at").count(),"devolve": dist.filter(is_return=True).count(),})
    elif type_filter == "diresaun":
        items = Diresaun.objects.all()
        for item in items:
            dist = Distribution.objects.filter(sub_departamento__departamento__diresaun=item)
            data.append({"name": item.name,"total": dist.count(),"existe": dist.filter(is_return=False).count(),
                "diak": dist.filter(kodition_return__name="Diak").count(),"aat": dist.filter(kodition_return__name="A'at").count(),
                "devolve": dist.filter(is_return=True).count(),})

    elif type_filter == "departamento":
        items = SubDepartamento.objects.all()
        for item in items:
            dist = Distribution.objects.filter(sub_departamento=item)
            data.append({"name": item.name,"total": dist.count(),"existe": dist.filter(is_return=False).count(),
                "diak": dist.filter(kodition_return__name="Diak").count(),"aat": dist.filter(kodition_return__name="A'at").count(),
                "devolve": dist.filter(is_return=True).count(),})

    context = {
        "data": data,'group':group,
        "type_filter": type_filter,
        "title": "Sumario Geral Distribuisaun",
        "legend": "Sumario Geral Distribuisaun",
        'link_antes': [{'link_name':"r-list",'link_text':"Rir"}],
    }
    return render(request, "Dist/sum_dist.html", context)