# Generated by Django 3.2.15 on 2022-09-22 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0002_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000024F8F00D280>', max_length=200),
        ),
    ]