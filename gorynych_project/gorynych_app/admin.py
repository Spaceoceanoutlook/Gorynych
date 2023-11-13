from django.contrib import admin
from .models import Word, Record


class WordAdmin(admin.ModelAdmin):
    search_fields = ('word',)


admin.site.register(Word, WordAdmin)
admin.site.register(Record)
