from django.contrib.admin import register, ModelAdmin
from django.contrib.auth import get_user_model
from suapintegration.models import LoginHistory


@register(get_user_model())
class SuapUserAdmin(ModelAdmin):
    list_display = ('username', 'name', 'email', 'campus', 'get_groups', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'campus', 'groups',)
    search_fields = ('username', 'name', 'social_name', 'email', 'scholar_email', 'academic_email')
    ordering = ('name',)

    readonly_fields = ['created_at', 'changed_at']

    def get_groups(self, instance):
        result = ', '.join([x.name for x in instance.groups.all()])
        return f'{result}'


@register(LoginHistory)
class LoginHistoryAdmin(ModelAdmin):
    list_display = ('login_at', 'user', 'ip')
    search_fields = ('user__name', 'login_at')
    ordering = ('login_at',)
    date_hierarchy = 'login_at'
