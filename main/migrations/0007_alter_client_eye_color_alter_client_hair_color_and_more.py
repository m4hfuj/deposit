# Generated by Django 4.1.7 on 2023-03-23 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_name_client_first_name_client_eye_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='eye_color',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='hair_color',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='height',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='weight',
            field=models.CharField(max_length=255),
        ),
    ]
