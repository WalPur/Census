from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class profile(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	surname = models.CharField(max_length=500)
	name = models.CharField(max_length=500)
	patronymic = models.CharField(max_length=500)

	SNILS_number = models.CharField(max_length=500)
	SNILS_ctrl = models.IntegerField()
	passportS = models.IntegerField()
	passportN = models.IntegerField()

	district = models.CharField(max_length=500)
	locality = models.CharField(max_length=500)
	address = models.CharField(max_length=500)

	phone = models.CharField(max_length=500)
	avatar = models.ImageField()

	group = models.IntegerField()
	childs = models.IntegerField()
