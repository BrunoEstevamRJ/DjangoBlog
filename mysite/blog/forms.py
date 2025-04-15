from django import forms
from .models import Post, Comment

# Formulário para Postagens
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'status', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['status'].initial = 'published'


# Formulário para comentários
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
