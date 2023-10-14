from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = (
        'login',
        'date_joined',

    )
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "first_name",
                "last_name",
                "login",
                "is_manager",
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','login',)

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Personal info',
         {'fields': (
             'role',
             "first_name",
             "last_name",
            'client',
            'fio',

             "is_manager",
             'email',
                "comment",
                "plain_password",



         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)


class RolePageInline(admin.TabularInline):
    model = RolePage
    extra = 0


class RoleAdmin(admin.ModelAdmin):
    model = Role
    inlines = [RolePageInline]


admin.site.register(Role, RoleAdmin)
admin.site.register(PagePermission)
admin.site.register(Page)

admin.site.register(User,UserAdmin)





