# Generated by Django 4.2.6 on 2023-11-17 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gorynych_app', '0007_alter_usergame_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergame',
            options={'verbose_name': 'Игра игрока', 'verbose_name_plural': 'Игры игроков'},
        ),
        migrations.AlterModelManagers(
            name='record',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='usergame',
            managers=[
            ],
        ),
    ]
