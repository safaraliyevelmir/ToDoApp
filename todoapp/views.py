from re import I
from django import template
from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from .models import Task, TaskShare
from .forms import TaskForm, CommentForm
from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.views import LoginRequiredMixin

User = get_user_model()

class CheckAccessMixin(object):

    def dispatch(self,request,*args,**kwargs):
        self.object = self.get_object()
        
        access = TaskShare.objects.filter(task=self.object).all()
        
        if any(x.user == request.user and x.request==True for x in access) or self.object.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('index')

class TaskDetail(LoginRequiredMixin,CheckAccessMixin,DetailView):
    template_name = 'detail.html'
    model = Task


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            task = self.get_object()
            form.user = request.user
            form.task = task
            form.save()
        
            return redirect(reverse('task-detail',args=[task.pk]))

class TaskSharePageView(LoginRequiredMixin,CheckAccessMixin,DetailView):
    template_name = 'share.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["task_share"] = TaskShare.objects.filter(task=task)
        return context
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        task = self.get_object()
        user = User.objects.filter(email=email).first()
        if user and user != request.user:
            task_share =  TaskShare.objects.filter(task=task,user=user).first()
            if task_share:
                pass
            else:
                TaskShare.objects.create(task=task,user=user,status=user_type)
        else:
            pass

        return redirect(reverse('task-share',args=[task.pk]))

class TrashPageView(LoginRequiredMixin,TemplateView):
    template_name = 'trash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trashs"] = Task.objects.filter(is_deleted=True,user=self.  request.user).all() 
        return context

class MessagePageView(LoginRequiredMixin,TemplateView):
    template_name = 'message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = TaskShare.objects.filter(user=self.request.user,request=False)

        return context

class SharedTaskPageView(LoginRequiredMixin,TemplateView):
    template_name = 'shared_task.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = TaskShare.objects.filter(user=self.request.user,request=True).all()
        return context

class UpdateTaskPageView(LoginRequiredMixin,CheckAccessMixin,UpdateView):
    template_name = 'update.html'
    model = Task
    form_class= TaskForm


    


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
    print(request.META.get('HTTP_REFERER'))
    if task.user == request.user:
        if task.done == True:
            task.done = False
            task.save()
        else:
            task.done = True
            task.save()
    return redirect('index')

def restoreTask(request,pk):
    task = Task.objects.get(pk=pk)
    if task.user == request.user:
        task.is_deleted = False
        task.save()
    return redirect('trash')

def deleteTaskFromTrash(request,pk):
    task = Task.objects.get(pk=pk)
    if task.user == request.user:
        task.delete()
    return redirect('trash')

def deleteTaskRequest(request,pk):
    request_task = TaskShare.objects.get(pk=pk)
    request_task.delete()
    redirect_url =  request.META.get('HTTP_REFERER')
    return redirect(redirect_url)

def acceptRequest(request,pk):
    message = TaskShare.objects.get(pk=pk)
    message.request = True
    message.save()
    return redirect('message')

def rejectRequest(request,pk):
    message = TaskShare.objects.get(pk=pk)
    message.delete()
    return redirect('message')