from django.contrib import admin
from .models import Comment, Task, TaskShare




class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','updated_at']

admin.site.register(Task,TaskAdmin)
admin.site.register(Comment)
admin.site.register(TaskShare)