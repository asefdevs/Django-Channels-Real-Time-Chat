# Generated by Django 5.0 on 2023-12-28 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room_created_at_room_first_user_room_second_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
