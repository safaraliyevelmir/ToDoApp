from os import name
from django.urls import path
from .views import MessagePageView, SharedTaskPageView, TaskDetail, TaskSharePageView, TrashPageView, UpdateTaskPageView, acceptRequest, addTask, deleteTask, deleteTaskFromTrash, deleteTaskRequest, doneTask, rejectRequest, restoreTask

urlpatterns = [
    path('add-task/',addTask,name='add-task'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task-detail'),
    path('delete-task/<int:pk>',deleteTask,name='delete-task'),
    path('update-task/<int:pk>',UpdateTaskPageView.as_view(),name='update-task'),
    path('done-task/<int:pk>/',doneTask,name='task-done'),
    path('task-share/<int:pk>/',TaskSharePageView.as_view(),name='task-share'),
    path('trash/',TrashPageView.as_view(),name='trash'),
    path('restore/<int:pk>',restoreTask,name='restore-task'),
    path('delete-trash/<int:pk>',deleteTaskFromTrash,name='delete-task-trash'),
    path('message/',MessagePageView.as_view(),name='message'),
    path('request-accept/<int:pk>',acceptRequest,name='accept-request'),
    path('reject-request/<int:pk>',rejectRequest,name='reject-request'),
    path('shared-task/',SharedTaskPageView.as_view(),name='shared-task'),
    path('delete-task-request/<int:pk>',deleteTaskRequest,name='delete-task-request'),
    

]
