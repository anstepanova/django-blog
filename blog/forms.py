from django import forms
from django.core.exceptions import ValidationError
from .models import Tag, Post


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "create".')
        if Tag.objects.filter(slug__iexact=new_slug).count() != 0:
            raise ValidationError(f'Slug must be unique. We have "{new_slug}" slug already.')
        return new_slug


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'slug', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(item['id'], item['title']) for item in Tag.objects.all().order_by('title').values()]
        self.fields['tags'] = forms.MultipleChoiceField(
            choices=choices,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'})
        )

