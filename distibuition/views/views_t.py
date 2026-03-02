from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Gabinete, SubGabinete, Diresaun, Departamento, SubDepartamento, Distribution

@login_required
def summaryDistribusi(request):
    def get_stats(filter_kwargs):
        qs = Distribution.objects.filter(**filter_kwargs)
        total   = qs.count()
        existe  = qs.filter(is_return=False).count()
        diak    = qs.filter(is_return=False, kodition_return__isnull=True).count()
        aat     = qs.filter(is_return=False).exclude(kodition_return__isnull=True).count()
        devolve = qs.filter(is_return=True).count()
        return {'total': total, 'existe': existe, 'diak': diak, 'aat': aat, 'devolve': devolve}

    # --- Gabinete ---
    gabinete_data = []
    for g in Gabinete.objects.all():
        stats = get_stats({'sub_gabinete__gabinete': g})
        gabinete_data.append({'obj': g, **stats})

    # --- Diresaun ---
    diresaun_data = []
    for d in Diresaun.objects.all():
        stats = get_stats({'sub_departamento__departamento__diresaun': d})
        diresaun_data.append({'obj': d, **stats})

    # --- SubGabinete + SubDepartamento gabung ---
    sub_gabinete_data = []
    for sg in SubGabinete.objects.select_related('gabinete').all():
        stats = get_stats({'sub_gabinete': sg})
        sub_gabinete_data.append({'obj': sg, 'parent': sg.gabinete.name, 'type': 'Gabinete', **stats})

    sub_departamento_data = []
    for sd in SubDepartamento.objects.select_related('departamento').all():
        stats = get_stats({'sub_departamento': sd})
        sub_departamento_data.append({'obj': sd, 'parent': sd.departamento.name, 'type': 'Departamento', **stats})

    # Gabung sub_gabinete + sub_departamento
    sub_all = sub_gabinete_data + sub_departamento_data

    context = {
        'gabinete_data': gabinete_data,
        'diresaun_data': diresaun_data,
        'sub_all': sub_all,
        'title': 'Sumario Distribuisaun Assets',
        'legend': 'Sumario Distribuisaun Assets Tuir Gabinete/Unidade',
    }
    return render(request, 'Dist/summary_distribusi.html', context)


# --- Detail SubGabinete ---
@login_required
def detailSubGabinete(request, gabinete_id):
    gabinete = get_object_or_404(Gabinete, id=gabinete_id)
    
    def get_stats(filter_kwargs):
        qs = Distribution.objects.filter(**filter_kwargs)
        return {
            'total':   qs.count(),
            'existe':  qs.filter(is_return=False).count(),
            'diak':    qs.filter(is_return=False, kodition_return__isnull=True).count(),
            'aat':     qs.filter(is_return=False).exclude(kodition_return__isnull=True).count(),
            'devolve': qs.filter(is_return=True).count(),
        }

    data = []
    for sg in SubGabinete.objects.filter(gabinete=gabinete):
        stats = get_stats({'sub_gabinete': sg})
        data.append({'obj': sg, **stats})

    context = {
        'parent': gabinete,
        'data': data,
        'legend': f'Sub Gabinete - {gabinete.name}',
    }
    return render(request, 'report/detail_sub.html', context)


# --- Detail Diresaun Geral ---
@login_required
def detailDiresaun(request, diresaun_id):
    diresaun = get_object_or_404(Diresaun, id=diresaun_id)

    def get_stats(filter_kwargs):
        qs = Distribution.objects.filter(**filter_kwargs)
        return {
            'total':   qs.count(),
            'existe':  qs.filter(is_return=False).count(),
            'diak':    qs.filter(is_return=False, kodition_return__isnull=True).count(),
            'aat':     qs.filter(is_return=False).exclude(kodition_return__isnull=True).count(),
            'devolve': qs.filter(is_return=True).count(),
        }

    data = []
    for dep in Departamento.objects.filter(diresaun=diresaun):
        stats = get_stats({'sub_departamento__departamento': dep})
        data.append({'obj': dep, **stats})

    context = {
        'parent': diresaun,
        'data': data,
        'legend': f'Diresaun Geral - {diresaun.name}',
    }
    return render(request, 'report/detail_sub.html', context)


# --- Detail SubDepartamento ---
@login_required
def detailSubDepartamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)

    def get_stats(filter_kwargs):
        qs = Distribution.objects.filter(**filter_kwargs)
        return {
            'total':   qs.count(),
            'existe':  qs.filter(is_return=False).count(),
            'diak':    qs.filter(is_return=False, kodition_return__isnull=True).count(),
            'aat':     qs.filter(is_return=False).exclude(kodition_return__isnull=True).count(),
            'devolve': qs.filter(is_return=True).count(),
        }

    data = []
    for sd in SubDepartamento.objects.filter(departamento=departamento):
        stats = get_stats({'sub_departamento': sd})
        data.append({'obj': sd, **stats})

    context = {
        'parent': departamento,
        'data': data,
        'legend': f'Sub Departamento - {departamento.name}',
    }
    return render(request, 'report/detail_sub.html', context)