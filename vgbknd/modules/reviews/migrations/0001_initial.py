# Generated by Django 3.2.3 on 2021-06-11 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=50)),
                ('comment_ranking', models.CharField(max_length=255)),
                ('date', models.DateField(default='2021-08-17')),
                ('ranking', models.IntegerField()),
                ('touristic_place', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='places.touristicplace')),
                ('user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PictureReview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=300)),
                ('number', models.IntegerField()),
                ('review', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
            ],
        ),
    ]
