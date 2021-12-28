from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model

user = get_user_model()

STATUS_CHOICE = (
    ('Admin','Admin'),
    ('Spectator','Spectator')
)


class Task(models.Model):

    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    description = models.TextField(null=True,blank=True)
    reminder = models.BooleanField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(user,on_delete=models.CASCADE,null=True,blank=True)

    is_deleted = models.BooleanField(default=False)
    

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})
    


    def __str__(self):
        return self.title

class TaskShare(models.Model):

    user = models.ForeignKey(user,on_delete=models.CASCADE,related_name="user_share_task")
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='task_share')
    status = models.CharField(choices=STATUS_CHOICE,max_length=255)
    request = models.BooleanField(default=False)


    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} {self.task.title}"

class Comment(models.Model):
    
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='task_comment')
    comment = models.TextField()

    # moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.user.email