from django.contrib import admin
#Uncomment this for bad auto-admins
#from eve_sde import models


#for attr in dir(models):
#	m = getattr(models, attr)
#	if isinstance(m, type) and issubclass(m, models.models.Model):
#		try:
#			admin.site.register(m)
#		except Exception as e:
#			print e