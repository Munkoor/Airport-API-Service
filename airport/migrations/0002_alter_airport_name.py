# Generated by Django 4.2.6 on 2023-10-07 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
