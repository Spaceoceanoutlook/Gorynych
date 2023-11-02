from django.contrib import admin
from .models import Word


class WordAdmin(admin.ModelAdmin):
    search_fields = ('word',)


admin.site.register(Word, WordAdmin)
