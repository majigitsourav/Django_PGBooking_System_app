# Generated by Django 4.2.3 on 2023-08-19 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pg', '0004_alter_pg_property_image1_alter_pg_property_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pg',
            name='property_image1',
            field=models.ImageField(upload_to='property_images/'),
        ),
        migrations.AlterField(
            model_name='pg',
            name='property_image2',
            field=models.ImageField(upload_to='property_images/'),
        ),
        migrations.AlterField(
            model_name='pg',
            name='property_image3',
            field=models.ImageField(upload_to='property_images/'),
        ),
    ]
