from django.utils.translation import gettext as _
from django.contrib.admin import register, ModelAdmin, TabularInline
from django.contrib.auth import get_user_model
from suapintegration.models import LoginHistory


@register(LoginHistory)
class LoginHistoryAdmin(ModelAdmin):
    list_display = ('login_at', 'user', 'ip')
    search_fields = ('user__name', 'login_at')
    ordering = ('-login_at',)
    date_hierarchy = 'login_at'


class LoginHistoryInline(TabularInline):
    model = LoginHistory
    fields = ['login_at', 'ip']
    ordering = ['-login_at']
    readonly_fields = ['login_at', 'ip']
    extra = 0


class SuapUserMixix(object):
    list_display = ('username', 'name', 'email', 'campus', 'get_groups',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'campus', 'groups',) 
    search_fields = ('username', 'name', 'email')
    ordering = ('name',)
    readonly_fields = ['created_at', 'changed_at']
    inlines = [LoginHistoryInline]

    def get_groups(self, instance):
        result = ', '.join([x.name for x in instance.groups.all()])
        return f'{result}'

try:
    from tabbed_admin import TabbedModelAdmin
    @register(get_user_model())
    class SuapUserAdmin(TabbedModelAdmin):
        list_display = ('username', 'name', 'email', 'campus', 'get_groups')
        list_filter = ('is_staff', 'is_superuser', 'is_active', 'campus', 'groups') 
        search_fields = ('username', 'name', 'email')
        ordering = ['name']

        readonly_fields = ['created_at', 'changed_at', 'last_login']
        tabs = [
            (_('Names'), [(None, {'fields': ['username', 'campus', 'name', 'social_name']})]),
            (_('E-Mails'), [(None, {'fields': ['email', 'academic_email', 'scholar_email',]})]),
            (_('Permissions'), [(None, {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups']})]),
            (_('Dates'), [(None, {'fields': ['created_at', 'changed_at', 'last_login']}), LoginHistoryInline]),
        ]

        def get_groups(self, instance):
            result = ', '.join([x.name for x in instance.groups.all()])
            return f'{result}'
except ImportError:
    @register(get_user_model())
    class SuapUserAdmin(ModelAdmin):
        list_display = ('username', 'name', 'email', 'campus', 'get_groups',)
        list_filter = ('is_staff', 'is_superuser', 'is_active', 'campus', 'groups',) 
        search_fields = ('username', 'name', 'email')
        ordering = ('name',)
        inlines = (LoginHistoryInline,)

        readonly_fields = ['created_at', 'changed_at', ]
        fieldsets = [
            (None, {'fields': [('username', 'campus'), ('name', 'social_name'), ('created_at', 'changed_at',),]}),
            (_('E-Mails'), {'fields': ['email', 'academic_email', 'scholar_email',]}),
            (_('Permissions'), {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups',]})
        ]

        def get_groups(self, instance):
            result = ', '.join([x.name for x in instance.groups.all()])
            return f'{result}'
        pass
