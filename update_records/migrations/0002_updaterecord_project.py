# Generated by Django 5.1.4 on 2024-12-20 07:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('update_records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterecord',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='update_records', to='projects.project'),
            preserve_default=False,
        ),
    ]
