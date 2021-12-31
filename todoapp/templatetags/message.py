from django import template

register = template.Library()

from todoapp.models import TaskShare



@register.simple_tag(name='messageCount')
def messageCount(user):
    return TaskShare.objects.filter(user=user,request=False).count()


