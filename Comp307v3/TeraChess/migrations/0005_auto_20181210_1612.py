# Generated by Django 2.1.3 on 2018-12-10 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeraChess', '0004_auto_20181210_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='piece',
            old_name='moveSet',
            new_name='move_set',
        ),
        migrations.RenameField(
            model_name='piece',
            old_name='picture_hite',
            new_name='picture_white',
        ),
    ]