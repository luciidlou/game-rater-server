# Generated by Django 4.0.1 on 2022-02-07 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gameraterapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='categories',
            field=models.ManyToManyField(related_name='categories', through='gameraterapi.GameCategory', to='gameraterapi.Category'),
        ),
        migrations.AddField(
            model_name='game',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='year_released',
            field=models.PositiveIntegerField(),
        ),
    ]
