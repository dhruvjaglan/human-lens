# Generated by Django 5.0.6 on 2024-06-18 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifier', '0004_customuser_is_annotator'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='verifier.company'),
        ),
    ]