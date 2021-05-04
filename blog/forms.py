from django import forms
from django.forms import ModelForm

from .models import Post, Signup

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "class": "form-control",
        "placeholder": "Type your email address",
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )