# Generated by Django 5.0.7 on 2024-07-19 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_profileuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='status_assinatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.plano'),
        ),
    ]
