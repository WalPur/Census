# Generated by Django 2.2.10 on 2020-05-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default=123, upload_to=''),
            preserve_default=False,
        ),
    ]