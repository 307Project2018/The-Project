# Generated by Django 2.1.3 on 2018-12-10 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeraChess', '0002_auto_20181205_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='moveSet',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='pieceset',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
