# Generated by Django 4.1.3 on 2022-11-11 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0004_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='network',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unit_network', to='coreapp.network'),
        ),
    ]
