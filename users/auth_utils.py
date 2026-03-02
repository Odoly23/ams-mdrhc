from funsionario.models import Staff

def c_user_staff(user):
	objects = Staff.objects.filter(funsionariouser__user=user).prefetch_related('staffuser').first()
	obj = ""
	if objects: obj = objects
	return obj