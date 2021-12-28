from __future__ import absolute_import, unicode_literals
from datetime import timedelta, datetime
from .models import Task
from celery import shared_task
from celery.decorators import task


@shared_task
def delete_post():
    delta = datetime.today() - timedelta(minutes=3)
    delete_posts = Task.objects.filter(updated_at__gte=delta,is_deleted=True)
    delete_posts.delete()


