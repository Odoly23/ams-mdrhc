from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import TableStyle
import io

from .models import (
    Entity,
    Gabinete,
    SubGabinete,
    Diresaun,
    Departamento,
    SubDepartamento,
    Category,
    Brand,
    Model,
    Company,
    Source,
    Status,
    Position,
    Location,
    SubCategory
)

# ================================
# RESOURCE FOR IMPORT / EXPORT
# ================================
admin.site.register(SubCategory)
class BaseModelResource(resources.ModelResource):
    class Meta:
        abstract = True

class EntityResource(BaseModelResource):
    class Meta:
        model = Entity
        fields = ('name',)

class GabineteResource(BaseModelResource):
    class Meta:
        model = Gabinete
        fields = ('name', 'entity__name')

class CategoryResource(BaseModelResource):
    class Meta:
        model = Category
        fields = ('name',)

class BrandResource(BaseModelResource):
    class Meta:
        model = Brand
        fields = ('name', 'category__name')

class CompanyResource(BaseModelResource):
    class Meta:
        model = Company
        fields = ('name',)


# ================================
# ADMIN FOR MASTER DATA
# ================================

@admin.register(Entity)
class EntityAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EntityResource
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    actions = ['export_pdf']

    # ================================
    # EXPORT PDF
    # ================================

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["Name", "Created At", "Updated At"]]

        for entity in queryset:
            data.append([
                entity.name,
                str(entity.created_at),
                str(entity.updated_at),
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    export_pdf.short_description = "Export Selected to PDF"


@admin.register(Gabinete)
class GabineteAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = GabineteResource
    list_display = ('name', 'entity', 'created_at', 'updated_at')
    search_fields = ('name', 'entity__name')
    list_filter = ('entity', 'created_at')
    actions = ['export_pdf']

    # ================================
    # EXPORT PDF
    # ================================

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["Name", "Entity", "Created At", "Updated At"]]

        for gabinete in queryset:
            data.append([
                gabinete.name,
                gabinete.entity.name,
                str(gabinete.created_at),
                str(gabinete.updated_at),
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    export_pdf.short_description = "Export Selected to PDF"


@admin.register(Category)
class CategoryAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    actions = ['export_pdf']


@admin.register(Brand)
class BrandAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = BrandResource
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'created_at')
    actions = ['export_pdf']


@admin.register(Company)
class CompanyAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CompanyResource
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    actions = ['export_pdf']

# ================================
# REGISTER OTHER MODELS
# ================================

@admin.register(Diresaun)
class DiresaunAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'created_at', 'updated_at')
    search_fields = ('name', 'entity__name')
    list_filter = ('entity',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('name', 'diresaun', 'created_at', 'updated_at')
    search_fields = ('name', 'diresaun__name')
    list_filter = ('diresaun',)


@admin.register(SubDepartamento)
class SubDepartamentoAdmin(admin.ModelAdmin):
    list_display = ('name', 'departamento', 'created_at', 'updated_at')
    search_fields = ('name', 'departamento__name')
    list_filter = ('departamento',)



@admin.register(SubGabinete)
class SubGabineteAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['building', 'room']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    search_fields=['name', 'brand']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    search_fields=['name']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields=['name']