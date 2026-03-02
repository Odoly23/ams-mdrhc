from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import TableStyle
import io

from .models import StaffStatus, Staff, StaffPosition


# =====================================================
# RESOURCE
# =====================================================

class StaffStatusResource(resources.ModelResource):
    class Meta:
        model = StaffStatus
        fields = ("name",)


class StaffResource(resources.ModelResource):
    class Meta:
        model = Staff
        fields = (
            "emp_id",
            "name",
            "entity__name",
            "sub_gabinete__name",
            "sub_departamento__name",
            "status__name",
            "is_active",
        )


class StaffPositionResource(resources.ModelResource):
    class Meta:
        model = StaffPosition
        fields = (
            "staff__emp_id",
            "staff__name",
            "position__name",
        )


# =====================================================
# INLINE POSITION
# =====================================================

class StaffPositionInline(admin.TabularInline):
    model = StaffPosition
    extra = 1
    autocomplete_fields = ["position"]


# =====================================================
# STAFF STATUS ADMIN
# =====================================================

@admin.register(StaffStatus)
class StaffStatusAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StaffStatusResource
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


# =====================================================
# STAFF ADMIN
# =====================================================

@admin.register(Staff)
class StaffAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StaffResource

    list_display = (
        "emp_id",
        "name",
        "entity",
        "status",
        "is_active",
        "created_at",
    )

    search_fields = (
        "emp_id",
        "name",
        "entity__name",
        "sub_gabinete__name",
        "sub_departamento__name",
    )

    list_filter = (
        "entity",
        "status",
        "is_active",
        "sub_gabinete",
        "sub_departamento",
    )

    autocomplete_fields = [
        "entity",
        "sub_gabinete",
        "sub_departamento",
        "status",
        "user",
    ]

    inlines = [StaffPositionInline]

    actions = ["export_pdf"]

    # =========================
    # EXPORT PDF
    # =========================

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["EMP ID", "Name", "Entity", "Status", "Active"]]

        for staff in queryset:
            data.append([
                staff.emp_id,
                staff.name,
                staff.entity.name,
                staff.status.name,
                "Yes" if staff.is_active else "No",
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
# STAFF POSITION ADMIN
# =====================================================

@admin.register(StaffPosition)
class StaffPositionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StaffPositionResource

    list_display = ("staff", "position", "created_at")

    search_fields = (
        "staff__emp_id",
        "staff__name",
        "position__name",
    )

    list_filter = ("position",)

    autocomplete_fields = ["staff", "position"]