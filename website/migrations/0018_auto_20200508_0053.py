# Generated by Django 2.2.10 on 2020-05-07 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_profile_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dateOfBirth',
            field=models.DateField(blank=True, default='1900-01-01'),
        ),
    ]