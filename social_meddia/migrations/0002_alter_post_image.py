# Generated by Django 5.0.3 on 2024-03-26 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_meddia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='media'),
        ),
    ]
