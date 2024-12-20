# Generated by Django 5.1.3 on 2024-12-15 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0003_remove_administrative_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dateOfBirth',
            field=models.CharField(max_length=10),
        ),
        migrations.DeleteModel(
            name='Administrative',
        ),
    ]
