# Generated by Django 3.1.1 on 2020-10-07 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Low', 'Low'), ('Normal', 'Normal')], default='Normal', max_length=50, null=True),
        ),
    ]
