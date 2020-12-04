from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text='Required. Enter a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class NoteForm(forms.ModelForm):
    title = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Type your note here!'}))
    class Meta:
        model = Note
        fields = ('title', 'body')