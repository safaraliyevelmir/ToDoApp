from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import EmailInput
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class UserLoginForm(forms.Form):
    
    email = forms.CharField(widget=EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    def clean(self,  *args, **kwargs):
        
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_obj = User.objects.filter(email=email).first()
        
        if not user_obj:
            raise forms.ValidationError("Invalid credentials")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError('Invalid credentials')
            return super(UserLoginForm, self).clean(*args, **kwargs)            





class UserRegistrationForm(forms.ModelForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))


    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email':forms.EmailInput(attrs={'placeholder':'E-Mail'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["Password isn't match"],
                code="password_isn't match",
            )
        return password2


    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
