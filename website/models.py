from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()