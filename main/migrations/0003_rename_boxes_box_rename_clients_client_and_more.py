# Generated by Django 4.1.7 on 2023-03-18 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_emp_clients_employee_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Boxes',
            new_name='Box',
        ),
        migrations.RenameModel(
            old_name='Clients',
            new_name='Client',
        ),
        migrations.RenameModel(
            old_name='Employees',
            new_name='Employee',
        ),
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]