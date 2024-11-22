from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "post_image", "tags", "status"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Entrez un titre"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Entrez ici le contenu",
                }
            ),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
