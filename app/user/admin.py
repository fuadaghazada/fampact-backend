from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from scoring.models import Score
from .models import User, Family


class UserAdminInline(admin.StackedInline):
    model = User
    extra = 1


class UserAdmin(BaseUserAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'username',
        'verified_at',
        'family',
        'role',
        'score'
    )
    list_filter = ('is_superuser', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_superuser', 'verified_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name', 'email',)
    filter_horizontal = ()

    def score(self, instance):
        return Score.objects.calculate_user_score(instance)


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'score')
    inlines = [
        UserAdminInline
    ]

    def get_queryset(self, request):
        return Score.objects.public_leader_board_qs()

    def score(self, instance):
        return instance.score


admin.site.register(User, UserAdmin)
admin.site.register(Family, FamilyAdmin)
