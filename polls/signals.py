from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import Group




def create_profile_group(sender,instance,created,**kwargs):
	if created:
		group = Group.objects.get(name='customer')
		instance.groups.add(group)
		Customer.objects.create(user=instance,name=instance.username,email=instance.email)
		print("Profile Created")

post_save.connect(create_profile_group,sender=User)

		