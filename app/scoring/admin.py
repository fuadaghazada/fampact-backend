from django.contrib import admin

from .models import Score


class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'score',
        'user',
        'task'
    )
    list_filter = ()
    search_fields = (
        'task__title',
        'task__description',
    )


admin.site.register(Score, ScoreAdmin)
