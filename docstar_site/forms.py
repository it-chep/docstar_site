from django import forms
from docstar_site.models import Speciallity, Doctor, City

class UpdateDoc(forms.ModelForm):
    avatar = forms.ImageField(label='Ваше фото', localize=False)

    class Meta:
        model = Doctor
        fields = ("avatar", )


class DoctorSearchForm(forms.Form):
    specialty = forms.ModelChoiceField(queryset=Speciallity.objects.all(), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(DoctorSearchForm, self).__init__(*args, **kwargs)

