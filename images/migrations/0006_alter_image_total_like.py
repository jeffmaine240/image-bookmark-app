# Generated by Django 4.0 on 2024-09-02 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_alter_image_total_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='total_like',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
