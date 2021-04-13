from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MinimalModel

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age', )}),) # 管理サイトの編集画面にageを追加
    list_display = ['username', 'email', 'age']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MinimalModel)