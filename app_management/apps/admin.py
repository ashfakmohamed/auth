from django.contrib import admin

from .models import App, Task


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "sub_category", "points")
    search_fields = ("name", "category", "sub_category")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "app", "completed", "created_at", "approved_at")
    list_filter = ("completed", "app")
    search_fields = ("user__username", "app__name")
    readonly_fields = ("created_at", "approved_at")
