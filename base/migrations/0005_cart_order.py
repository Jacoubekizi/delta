# Generated by Django 5.1.7 on 2025-05-12 22:41

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_bouquet_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bouquets', models.ManyToManyField(to='base.bouquet')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('ذكر', 'ذكر'), ('أنثى', 'أنثى')], max_length=20)),
                ('birthdate', models.DateField()),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='SY', unique=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('bouquets', models.ManyToManyField(to='base.bouquet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
