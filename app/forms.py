from django import forms

from app.models import ImageModel


class ImageForm(forms.ModelForm):
    link = forms.URLField(required=False)
    class Meta:
        model = ImageModel
        exclude = ()