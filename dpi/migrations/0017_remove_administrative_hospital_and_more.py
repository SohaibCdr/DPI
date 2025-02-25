# Generated by Django 5.1.3 on 2024-12-21 11:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0016_remove_hospital_actors_administrative_hospital_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrative',
            name='Hospital',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='Hospital',
        ),
        migrations.RemoveField(
            model_name='laborantin',
            name='Hospital',
        ),
        migrations.RemoveField(
            model_name='nurse',
            name='Hospital',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='Hospital',
        ),
        migrations.RemoveField(
            model_name='radiologist',
            name='Hospital',
        ),
        migrations.AddField(
            model_name='administrative',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='administratives', to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='laborantin',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laborantins', to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='nurse',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nurses', to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='patient',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='radiologist',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radilogists', to='dpi.hospital'),
        ),
    ]
