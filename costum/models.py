from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# =====================================================
# BASE MODEL
# =====================================================

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_updated"
    )
    updated_at = models.DateTimeField(null=True, blank=True)

    deleted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_deleted"
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def soft_delete(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    class Meta:
        abstract = True


# =====================================================
# INSTITUTION STRUCTURE
# =====================================================

class Entity(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Gabinete(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubGabinete(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    gabinete = models.ForeignKey(Gabinete, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Diresaun(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Departamento(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    diresaun = models.ForeignKey(Diresaun, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubDepartamento(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# =====================================================
# MASTER DATA (ASSET LOOKUPS)
# =====================================================

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Model(BaseModel):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Company(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Source(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Status(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Location(BaseModel):
    building = models.CharField(max_length=200)
    room = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.building} - {self.room}"