# Generated by Django 3.0.3 on 2020-02-21 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='number_address',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
