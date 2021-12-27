from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from todoapp.forms import TaskForm
from todoapp.models import Task

class LoginRequiredMixin(object):
    
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)

class IndexPageView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()
        context["tasks"] = Task.objects.filter(is_deleted=False, user=self.request.user).all()
        return context
    
