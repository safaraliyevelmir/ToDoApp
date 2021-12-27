from django import forms
from .models import Comment, Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title','deadline','description','reminder']
    
    
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'deadline':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'reminder':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'})

        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment':forms.Textarea(attrs={'class':'form-control'})
        }
    