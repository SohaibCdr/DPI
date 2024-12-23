# Generated by Django 5.1.3 on 2024-12-21 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0015_hospital_actors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='actors',
        ),
        migrations.AddField(
            model_name='administrative',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='laborantin',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='nurse',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='patient',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dpi.hospital'),
        ),
        migrations.AddField(
            model_name='radiologist',
            name='Hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dpi.hospital'),
        ),
    ]