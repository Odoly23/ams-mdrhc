from django.db import models
from costum.models import BaseModel
from django.contrib.auth.models import User
from assets.models import Equipment
# Create your models here.

class Maintenance(BaseModel):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    performed_by = models.CharField(max_length=200)

    def __str__(self):
        return f"Maintenance - {self.equipment}"