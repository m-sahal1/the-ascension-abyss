# Generated by Django 4.1.5 on 2023-06-22 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_elevator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevator',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
