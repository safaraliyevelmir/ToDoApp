from django.contrib import admin
from .models import Comment, Task, TaskShare


admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(TaskShare)