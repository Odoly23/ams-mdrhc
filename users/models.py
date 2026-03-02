from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import uuid
from users.utils_upload import upload_profile
from funsionario.models import Staff

import datetime
class ProfileType(models.Model):
	type = models.CharField(max_length=100)
	number = models.IntegerField()
	deskrisaun = models.TextField()
	is_active = models.BooleanField(default=True)
	user_created = models.ForeignKey(User,related_name="ptusercreated", on_delete=models.CASCADE, null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	user_updated = models.ForeignKey(User,related_name="ptuserupdated", on_delete=models.CASCADE, null=True,blank=True)
	date_updated = models.DateTimeField(auto_now_add=False,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)	

	def __str__(self):
		template = '{0.type}'
		return template.format(self)

class Profile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)
	type = models.ForeignKey(ProfileType,on_delete=models.CASCADE,related_name='pt',null=True,blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile",null=True,blank=True)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)
	id_number = models.CharField(max_length=50, verbose_name='Nu. Identificacao', null=True, blank=True)
	pob = models.CharField(max_length=50, verbose_name='Fatin Moris', null=True, blank=True)
	email = models.EmailField(max_length=100, verbose_name='Email', null=True, blank=True)
	dob = models.DateField(verbose_name='Data Moris', null=True, blank=True)
	sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=6, null=True, blank=True)
	image = models.ImageField(upload_to=upload_profile, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','gif'])], verbose_name="Upload Imajen")
	user_created = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_profile_created",null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	password_reset_token = models.TextField(null=True)
	new_activate_token = models.TextField(null=True)

	def getAge(self):
		if self.dob:
			return datetime.date.today().year - self.dob.year
		else:
			return 0
			
	def getTotalLogin(self):
		return AuditLogin.objects.filter(user=self.user).count()
		
	def __str__(self):
		template = '{0.user}, {0.first_name} {0.last_name} | {0.type}'
		return template.format(self)


class AuditLogin(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="audituserlogin")
	login_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

		
	def __str__(self):
		template = '{0.user}, {0.login_time}'
		return template.format(self)
