# Generated by Django 3.1 on 2020-10-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work_order',
            name='tagnumber',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
