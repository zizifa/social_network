# Generated by Django 4.1.7 on 2023-03-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='blank-profile-picture', upload_to='media/profile_images'),
        ),
    ]
