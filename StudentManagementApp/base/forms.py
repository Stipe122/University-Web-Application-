from django.forms import ModelForm
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Subject, Role, User

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        role_professor = Role.objects.get(name='Professor')
        professors = User.objects.filter(role=role_professor)
        self.fields['lecturer'].queryset = professors

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'status', 'role']

    def clean_password(self):
        password = make_password(self.cleaned_data.get('password'))
        return password
    

class EditUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'status', 'role']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        return self.instance.password  # return the existing password if not provided
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        return status if status else self.instance.status
    
    def clean_role(self):
        role = self.cleaned_data.get('role')
        return role if role else self.instance.role