# Generated by Django 4.2.6 on 2023-12-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gorynych_app', '0013_statictics'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statictics',
            options={'verbose_name': 'Статистика', 'verbose_name_plural': 'Статистика'},
        ),
        migrations.AddField(
            model_name='statictics',
            name='number_of_games',
            field=models.IntegerField(default=0, verbose_name='Количество игр'),
        ),
    ]
