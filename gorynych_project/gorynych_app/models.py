from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=99, verbose_name='Слова')
    objects = models.Manager()

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'
