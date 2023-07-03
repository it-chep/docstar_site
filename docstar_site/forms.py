from django import forms
from .models import *


class UpdateDoc(forms.ModelForm):
    avatar = forms.ImageField(label='Ваше фото', localize=False)

    class Meta:
        model = Doctor
        fields = ("avatar", )


