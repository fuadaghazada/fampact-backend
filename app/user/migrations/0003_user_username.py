# Generated by Django 3.1.2 on 2021-02-21 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210220_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='admin', max_length=255, unique=True, verbose_name='Username'),
            preserve_default=False,
        ),
    ]
