from django import forms
from .models import Post, Photo

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['url']
