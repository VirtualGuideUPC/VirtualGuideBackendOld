# Generated by Django 3.2.3 on 2021-06-01 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210531_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
