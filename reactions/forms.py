from django import forms
from .models import Reaction

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['type']

    def clean(self):
        cleaned_data = super().clean()
        user = self.initial['user']
        post = self.initial['post']
        type = cleaned_data.get('type')

        if Reaction.objects.filter(user=user, post=post, type=type).exists():
            raise forms.ValidationError("You have already reacted with this type.")
        return cleaned_data
