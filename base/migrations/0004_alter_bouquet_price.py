# Generated by Django 5.1.7 on 2025-04-04 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_bouquet_medical_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bouquet',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
