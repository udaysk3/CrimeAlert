# Generated by Django 4.1.5 on 2024-02-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_scamreport_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scamreport',
            name='image',
            field=models.ImageField(upload_to='scam_images/'),
        ),
    ]