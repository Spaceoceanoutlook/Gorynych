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
    object = models.Manager()

    def __str__(self):
        return f'{self.record}'

    class Meta:
        verbose_name = 'Рекорд'
        verbose_name_plural = 'Рекорды'

