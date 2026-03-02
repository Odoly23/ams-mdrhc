import os, hashlib
# import numpy as np
from uuid import uuid4

def upload_profile(instance, filename):
	upload_to = 'users_files/'
	field = 'Foto_Profile'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.first_name,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

