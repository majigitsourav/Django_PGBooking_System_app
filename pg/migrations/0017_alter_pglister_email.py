# Generated by Django 4.2.3 on 2023-08-29 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pg', '0016_alter_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pglister',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]