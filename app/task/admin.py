from django.contrib import admin

from .models import (Task, TaskStatusLog)


class TaskStatusLogAdmin(admin.StackedInline):
    model = TaskStatusLog
    extra = 1


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'created_by',
        'assigned_to',
        'deadline',
        'started_at',
        'finished_at',
        'created_at',
        'updated_at'
    )
    list_filter = ('status',)
    search_fields = (
        'id',
        'title',
        'description',
    )
    inlines = [
        TaskStatusLogAdmin,
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(TaskAdmin, self).save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
