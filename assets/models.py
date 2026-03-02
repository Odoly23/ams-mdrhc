from django.db import models
from costum.models import BaseModel, Company, Category, Brand, Model, Source, Status, Location, SubCategory
# =========================================================
# PROCUREMENT (RIR / INCOMING)
# =========================================================
class RIR(BaseModel):
    rir_no = models.CharField(max_length=50, unique=True)
    invoice_no = models.CharField(max_length=50)
    container_no = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    hashed = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.rir_no



class RIRItem(BaseModel):
    PURCHASE_TYPE_CHOICES = [
        ("Sosa", "Sosa"),
        ("Apoiu", "Apoiu"),
    ]

    rir = models.ForeignKey(RIR, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    purchase_type = models.CharField(max_length=10, choices=PURCHASE_TYPE_CHOICES, default="Sosa")
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    donor_name = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    hashed = models.CharField(max_length=32, null=True)
    def clean(self):
        from django.core.exceptions import ValidationError

        if self.purchase_type == "Sosa" and not self.source:
            raise ValidationError("Karik sosa, Tenke Prense Source.")
        if self.purchase_type == "Apoiu" and not self.donor_name:
            raise ValidationError("Karik Apoiu, tenke prense Doasaun.")

    def __str__(self):
        return f"{self.rir.rir_no} - {self.category.name} ({self.purchase_type})"

# =========================================================
# EQUIPMENT
# =========================================================

class Equipment(BaseModel):
    rir_item = models.ForeignKey(RIRItem, on_delete=models.CASCADE, related_name="equipments")
    barcode = models.CharField(max_length=50, unique=True)
    serial_no = models.CharField(max_length=100, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    purchase_year = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="equipment/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_disposed = models.BooleanField(default=False)

    def __str__(self):
        return self.barcode