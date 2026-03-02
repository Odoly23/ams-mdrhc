from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import TableStyle
import io

from .models import Distribution, EquipmentMovement



# =====================================================
# DISTRIBUTION RESOURCE
# =====================================================

class DistributionResource(resources.ModelResource):
    class Meta:
        model = Distribution
        fields = (
            "entity__name",
            "sub_gabinete__name",
            "sub_departamento__name",
            "equipment__barcode",
            "staff__emp_id",
            "date_assigned",
            "date_returned",
            "is_approved",
            "is_confirmed",
            "is_return",
        )


# =====================================================
# EQUIPMENT MOVEMENT RESOURCE
# =====================================================

class EquipmentMovementResource(resources.ModelResource):
    class Meta:
        model = EquipmentMovement
        fields = (
            "equipment__barcode",
            "from_location__building",
            "to_location__building",
            "moved_by__username",
            "note",
            "created_at",
        )


# =====================================================
# DISTRIBUTION ADMIN
# =====================================================

@admin.register(Distribution)
class DistributionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DistributionResource

    list_display = (
        "equipment",
        "staff",
        "date_assigned",
        "date_returned",
        "is_approved",
        "is_confirmed",
        "is_return",
    )

    search_fields = (
        "staff__emp_id",
        "staff__name",
        "equipment__barcode",
        "equipment__serial_no",
        "sub_gabinete__name",
        "sub_departamento__name",
    )

    list_filter = (
        "is_approved",
        "is_confirmed",
        "is_return",
        "entity",
        "sub_gabinete",
        "sub_departamento",
    )

    autocomplete_fields = ["entity", "sub_gabinete", "sub_departamento", "equipment", "staff"]

    actions = ["export_pdf"]

    # =========================
    # EXPORT PDF
    # =========================

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["Equipment", "Staff", "Date Assigned", "Date Returned", "Approved"]]

        for distribution in queryset:
            data.append([
                distribution.equipment.barcode,
                distribution.staff.name,
                distribution.date_assigned,
                distribution.date_returned if distribution.date_returned else "Not Returned",
                "Yes" if distribution.is_approved else "No",
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(buffer, content_type="application/pdf")

    export_pdf.short_description = "Export Selected to PDF"


# =====================================================
# EQUIPMENT MOVEMENT ADMIN
# =====================================================

@admin.register(EquipmentMovement)
class EquipmentMovementAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EquipmentMovementResource

    list_display = (
        "equipment",
        "from_location",
        "to_location",
        "moved_by",
        "note",
        "created_at",
    )

    search_fields = (
        "equipment__barcode",
        "equipment__serial_no",
        "from_location__building",
        "to_location__building",
        "moved_by__username",
    )

    list_filter = ("from_location", "to_location", "moved_by")

    autocomplete_fields = ["equipment", "from_location", "to_location", "moved_by"]

    actions = ["export_pdf"]

    # =========================
    # EXPORT PDF
    # =========================

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["Equipment", "From Location", "To Location", "Moved By", "Note"]]

        for movement in queryset:
            data.append([
                movement.equipment.barcode,
                movement.from_location.building,
                movement.to_location.building,
                movement.moved_by.username,
                movement.note if movement.note else "No Note",
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(buffer, content_type="application/pdf")

    export_pdf.short_description = "Export Selected to PDF"


# Aksi untuk Soft Delete
def soft_delete(self, request, queryset):
    for obj in queryset:
        obj.soft_delete(request.user)

soft_delete.short_description = "Soft Delete Selected"

# Tambahkan ke `actions` di Admin
actions = ["export_pdf", "soft_delete"]