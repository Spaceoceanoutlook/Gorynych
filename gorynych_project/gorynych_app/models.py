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


class UserGame(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    game = models.BinaryField()
    record = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Игра игрока'
        verbose_name_plural = 'Игры игроков'
