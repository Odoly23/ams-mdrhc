from django.db import models
from django.contrib.auth.models import User
from costum.models import BaseModel, Company, Category, Brand, Model, Source, Entity, SubGabinete, SubDepartamento, Status, Location
from assets.models import Equipment 
from funsionario.models import Staff

class Distribution(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="dist_members", verbose_name='Entidade')
    sub_gabinete = models.ForeignKey(SubGabinete, on_delete=models.CASCADE, null=True, blank=True, related_name="dist_members", verbose_name="Gabinete")
    sub_departamento = models.ForeignKey(SubDepartamento, on_delete=models.CASCADE, null=True, blank=True, related_name="dist_members", verbose_name="Departamento")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_assigned = models.DateField()
    date_returned = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)
    kodition_return = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True)
    def __str__(self):
        return f"{self.equipment} → {self.staff}"


class EquipmentMovement(BaseModel):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_movements", verbose_name="fatin_Atual")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_movements", verbose_name="Fatin_Tuir_Mai")
    moved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    hashed = models.CharField(max_length=32, null=True)
    def __str__(self):
        return f"Muda {self.equipment}"


