# Generated by Django 2.2.10 on 2020-05-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_profile_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='code',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]