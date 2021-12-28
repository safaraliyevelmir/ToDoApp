from django.urls import path
from .views import TaskDetail, TaskSharePageView, TrashPageView, addTask, deleteTask, deleteTaskFromTrash, doneTask, restoreTask

urlpatterns = [
    path('add-task/',addTask,name='add-task'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task-detail'),
    path('delete-task/<int:pk>',deleteTask,name='delete-task'),
    path('done-task/<int:pk>/',doneTask,name='task-done'),
    path('task-share/<int:pk>/',TaskSharePageView.as_view(),name='task-share'),
    path('trash/',TrashPageView.as_view(),name='trash'),
    path('restore/<int:pk>',restoreTask,name='restore-task'),
    path('delete-trash/<int:pk>',deleteTaskFromTrash,name='delete-task-trash')

]
