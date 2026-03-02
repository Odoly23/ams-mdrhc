from django.db import models
from django.contrib.auth.models import User
from costum.models import BaseModel, Entity, SubGabinete, SubDepartamento, Position

# =====================================================
# STAFF STATUS
# =====================================================

class StaffStatus(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Staff Statuses"

    def __str__(self):
        return self.name


# =====================================================
# STAFF
# =====================================================

class Staff(BaseModel):
    emp_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="staff_members")
    sub_gabinete = models.ForeignKey(SubGabinete, on_delete=models.CASCADE, null=True, blank=True, related_name="staff_members")
    sub_departamento = models.ForeignKey(SubDepartamento, on_delete=models.CASCADE, null=True, blank=True, related_name="staff_members" )
    status = models.ForeignKey(StaffStatus, on_delete=models.CASCADE, related_name="staff_members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="staff_profile" )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["emp_id"]

    def __str__(self):
        return f"{self.emp_id} - {self.name}"



# =====================================================
# STAFF POSITION
# =====================================================
class StaffUser(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name="funsionariouser")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        template = '{0.staff} - {0.user}'
        return template.format(self)

# =====================================================
# STAFF POSITION
# =====================================================

class StaffPosition(BaseModel):
    staff = models.ForeignKey(Staff,  on_delete=models.CASCADE, related_name="positions")
    position = models.ForeignKey(Position,  on_delete=models.CASCADE, related_name="staff_holders")

    class Meta:
        unique_together = ("staff", "position")
        verbose_name = "Staff Position"
        verbose_name_plural = "Staff Positions"

    def __str__(self):
        return f"{self.staff.name} - {self.position.name}"