# Generated by Django 4.2.6 on 2024-07-11 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_system', '0007_rename_category_addvehicle_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addvehicle',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
