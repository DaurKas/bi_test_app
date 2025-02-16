# Generated by Django 5.1.4 on 2025-01-06 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='discount_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='discount',
            name='discount_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='discount',
            name='discount_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
