from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import TableStyle
import io
from .models import RIR, RIRItem, Equipment


# ================================
# RESOURCE FOR IMPORT / EXPORT
# ================================

class RIRResource(resources.ModelResource):
    class Meta:
        model = RIR
        fields = ('rir_no', 'invoice_no', 'container_no', 'company__name', 'arrival_date', 'is_approved', 'description')


class RIRItemResource(resources.ModelResource):
    class Meta:
        model = RIRItem
        fields = ('rir__rir_no', 'category__name', 'brand__name', 'model__name', 'purchase_type', 'source__name', 'donor_name', 'quantity', 'unit_cost', 'description')


class EquipmentResource(resources.ModelResource):
    class Meta:
        model = Equipment
        fields = ('barcode', 'rir_item__rir__rir_no', 'serial_no', 'status__name', 'location__building', 'purchase_year', 'is_active', 'is_disposed')


# ================================
# ADMIN FOR RIR
# ================================

@admin.register(RIR)
class RIRAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RIRResource
    list_display = ('rir_no', 'invoice_no', 'company', 'arrival_date', 'is_approved', 'created_at', 'updated_at')
    search_fields = ('rir_no', 'invoice_no', 'company__name', 'arrival_date')
    list_filter = ('company', 'is_approved', 'arrival_date')
    actions = ['export_pdf']

    # ================================
    # EXPORT PDF
    # ================================

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["RIR No", "Invoice No", "Company", "Arrival Date", "Approved", "Created At"]]

        for rir in queryset:
            data.append([
                rir.rir_no,
                rir.invoice_no,
                rir.company.name,
                str(rir.arrival_date),
                "Yes" if rir.is_approved else "No",
                str(rir.created_at),
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


# ================================
# ADMIN FOR RIR ITEM
# ================================

@admin.register(RIRItem)
class RIRItemAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RIRItemResource
    list_display = ('rir', 'category', 'brand', 'model', 'purchase_type', 'quantity', 'unit_cost', 'created_at', 'updated_at')
    search_fields = ('rir__rir_no', 'category__name', 'brand__name', 'model__name')
    list_filter = ('purchase_type', 'rir__company', 'category', 'brand', 'created_at')


# ================================
# ADMIN FOR EQUIPMENT
# ================================

@admin.register(Equipment)
class EquipmentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EquipmentResource
    list_display = ('barcode', 'rir_item', 'serial_no', 'status', 'location', 'purchase_year', 'is_active', 'is_disposed', 'created_at', 'updated_at')
    search_fields = ('barcode', 'rir_item__rir_no', 'serial_no', 'status__name', 'location__building')
    list_filter = ('status', 'location', 'is_active', 'purchase_year', 'created_at')