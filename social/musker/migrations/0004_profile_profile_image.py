# Generated by Django 4.2.2 on 2023-07-05 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0003_meep'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]