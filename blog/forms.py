from django import forms
from django.contrib.auth.models import User
from .models import Posts




# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email']


class CreatePostsForm(forms.ModelForm):
    class Meta:
        model = Posts

        fields = ['title', 'content']


class UpdatePostsForm(forms.ModelForm):
    class Meta:
        model = Posts

        fields = ['title', 'content']


class DeletePostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = []
