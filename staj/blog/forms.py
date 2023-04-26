from django import forms

from blog.models import Post, Comment


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Поиск' )
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']
        widgets = {'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        post_pk = kwargs.pop('post_pk', None)
        super().__init__(*args, **kwargs)
        self.post_pk = post_pk

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.post_id = self.post_pk
        if commit:
            comment.save()
        return comment

class FavoriteForm(forms.Form):
    note = forms.CharField(max_length=30, required=True, label='Заметка')