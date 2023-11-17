from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=99, verbose_name='Слова', unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'


class Record(models.Model):
    record = models.IntegerField(verbose_name='Рекорд')
    objects = models.Manager()

    def __str__(self):
        return f'{self.record}'

    class Meta:
        verbose_name = 'Рекорд'
        verbose_name_plural = 'Рекорды'


class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    game = models.BinaryField()
    objects = models.Manager()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Игра игрока'
        verbose_name_plural = 'Игры игроков'
