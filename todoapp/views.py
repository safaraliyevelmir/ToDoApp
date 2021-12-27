from django.shortcuts import redirect, render
from .models import Task, TaskShare
from .forms import TaskForm, CommentForm
from django.views.generic import DetailView
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.views import LoginRequiredMixin

User = get_user_model()


class TaskDetail(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    model = Task


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def get (self,request,*args,**kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.user != self.object.user:
            return redirect('index')
        else:
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            task = self.get_object()
            form.user = request.user
            form.task = task
            form.save()
        
            return redirect(reverse('task-detail',args=[task.pk]))

class TaskSharePageView(LoginRequiredMixin,DetailView):
    template_name = 'share.html'
    model = Task

    def get (self,request,*args,**kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.user != self.object.user:
            return redirect('index')
        else:
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        task = self.get_object()
        task_share = User.objects.filter(email=email).first()
        if task_share:
            TaskShare.objects.create(task=task,user=task_share)
        else:
            pass

        return redirect(reverse('task-share',args=[task.pk]))

def deleteTask(request,pk):
    
    task = Task.objects.get(pk=pk)

    if task.user == request.user:
        task.is_deleted = True
        task.save()
        return redirect('index')
    else: 
        return redirect('index')

def addTask(request):
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
    return redirect('index')

def doneTask(request,pk):
    task = Task.objects.get(pk=pk)
    if task.done == True:
        task.done = False
        task.save()
    else:
        task.done = True
        task.save()
    return redirect('index')