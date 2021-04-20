from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Like, MinimalModel, ThingStatus

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('image', )}),) # 管理サイトの編集画面にageを追加
    list_display = ['username', 'email', 'image']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MinimalModel)
admin.site.register(ThingStatus)
admin.site.register(Like)