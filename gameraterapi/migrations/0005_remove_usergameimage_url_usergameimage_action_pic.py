# Generated by Django 4.0.2 on 2022-02-10 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameraterapi', '0004_alter_usergamerating_datetime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergameimage',
            name='url',
        ),
        migrations.AddField(
            model_name='usergameimage',
            name='action_pic',
            field=models.ImageField(null=True, upload_to='actionimages'),
        ),
    ]