from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import TableStyle
import io
from .models import Profile, ProfileType, AuditLogin


# =====================================================
# PROFILETYPE RESOURCE
# =====================================================

class ProfileTypeResource(resources.ModelResource):
    class Meta:
        model = ProfileType
        fields = ("type", "number", "deskrisaun", "is_active", "user_created", "date_created")


# =====================================================
# PROFILE RESOURCE
# =====================================================

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        fields = (
            "user__username",
            "first_name",
            "last_name",
            "email",
            "dob",
            "sex",
            "staff__emp_id",
            "type__type",
            "type__number",
            "type__deskrisaun",
            "date_created",
        )


# =====================================================
# AUDIT LOGIN RESOURCE
# =====================================================

class AuditLoginResource(resources.ModelResource):
    class Meta:
        model = AuditLogin
        fields = ("user__username", "login_time")


# =====================================================
# PROFILE ADMIN
# =====================================================

@admin.register(Profile)
class ProfileAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProfileResource
    list_display = ("user", "first_name", "last_name", "email", "dob", "sex", "staff", "type", "date_created")
    search_fields = ("user__username", "first_name", "last_name", "email", "staff__emp_id")
    list_filter = ("sex", "type", "staff__sub_departamento", "date_created")
    autocomplete_fields = ["staff", "user", "type"]
    actions = ["export_pdf"]

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["User", "Name", "Email", "Date of Birth", "Type", "Date Created"]]

        for profile in queryset:
            data.append([
                profile.user.username,
                f"{profile.first_name} {profile.last_name}",
                profile.email,
                profile.dob,
                profile.type.type if profile.type else "N/A",
                profile.date_created,
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
# PROFILETYPE ADMIN
# =====================================================

@admin.register(ProfileType)
class ProfileTypeAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProfileTypeResource
    list_display = ("type", "number", "deskrisaun", "is_active", "user_created", "date_created")
    search_fields = ("type", "number", "deskrisaun", "user_created__username")
    list_filter = ("is_active", "date_created")
    actions = ["export_pdf"]

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["Type", "Number", "Description", "Is Active", "User Created", "Date Created"]]

        for profile_type in queryset:
            data.append([
                profile_type.type,
                profile_type.number,
                profile_type.deskrisaun,
                "Yes" if profile_type.is_active else "No",
                profile_type.user_created.username if profile_type.user_created else "N/A",
                profile_type.date_created,
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
# AUDIT LOGIN ADMIN
# =====================================================

@admin.register(AuditLogin)
class AuditLoginAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AuditLoginResource
    list_display = ("user", "login_time")
    search_fields = ("user__username",)
    list_filter = ("login_time",)
    actions = ["export_pdf"]

    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        data = [["User", "Login Time"]]

        for audit_login in queryset:
            data.append([
                audit_login.user.username,
                audit_login.login_time,
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