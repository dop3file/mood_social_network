from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        max_length=120,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleFormControlInput1', 'placeholder': 'Опишите ваше настроение', 'name': 'post_text', 'rows': 4}),
        required=True,
    )
    image = forms.FileField( 
                    label='',
                    widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'exampleFormControlInput1', 'placeholder': 'Аватарка', 'name': 'post_image'}),
                    required=False
                    )
    type_mood = forms.CharField(
        label='',
        widget=forms.Select(choices=(('Белый','Белый'), ('Черный','Черный')), attrs={'class': 'form-select form-select-sm', 'id': 'inlineFormCustomSelect'}))
    

    class Meta:
        model = Post
        fields = ['text', 'image', 'type_mood']