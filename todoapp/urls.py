from django.urls import path
from .views import TaskDetail, TaskSharePageView, addTask, deleteTask, doneTask

urlpatterns = [
    path('add-task/',addTask,name='add-task'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task-detail'),
    path('delete-task/<int:pk>',deleteTask,name='delete-task'),
    path('done-task/<int:pk>/',doneTask,name='task-done'),
    path('task-share/<int:pk>/',TaskSharePageView.as_view(),name='task-share')
]
