# Generated by Django 2.2.1 on 2019-08-28 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseRS', '0006_auto_20190828_0326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='stuCode',
            new_name='userIDCard',
        ),
        migrations.AlterField(
            model_name='user',
            name='subordinateClass',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
