from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	surname = models.CharField(max_length=500)
	name = models.CharField(max_length=500)
	patronymic = models.CharField(max_length=500)

	dateOfBirth = models.DateField(default='1900-01-01', blank=True)

	SNILS_number = models.CharField(max_length=500, blank=True)
	SNILS_ctrl = models.IntegerField(blank=True, default=0)
	passportS = models.IntegerField(blank=True, default=0)
	passportN = models.IntegerField(blank=True, default=0)

	district = models.CharField(max_length=500, blank=True)
	locality = models.CharField(max_length=500, blank=True)
	address = models.CharField(max_length=500, blank=True)

	phone = models.CharField(max_length=500, blank=True)

	group = models.IntegerField(blank=True, default=0)
	childs = models.IntegerField(blank=True, default=0)

	isActive = models.BooleanField(default=0)

	token = models.CharField(max_length=20)
	code = models.CharField(max_length=6, blank=True)
