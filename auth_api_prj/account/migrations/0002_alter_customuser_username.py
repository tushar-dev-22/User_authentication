# Generated by Django 4.1.6 on 2023-02-17 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
