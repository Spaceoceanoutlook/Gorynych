from django.contrib import admin
from .models import Word, UserGame, Statictics


class WordAdmin(admin.ModelAdmin):
    search_fields = ('word',)


admin.site.register(Word, WordAdmin)
admin.site.register(UserGame)
admin.site.register(Statictics)
