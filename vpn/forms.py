from django import forms

DATE_CHOICES = (
    ('day', 'За день'),
    ('week', 'За последнюю неделю'),
    ('30_days', 'За последние 30 дней'),
    ('all', 'Все'),
)


class ClientFilterForm(forms.Form):
    client_utm = forms.CharField(
        max_length=255, required=False, label='UTM клиента',
        widget=forms.TextInput(attrs={'placeholder': 'Введите UTM блогера текстом "readydoc"'})
    )
    client_date = forms.ChoiceField(choices=DATE_CHOICES, required=False, label='Дата клиента')


class BloggerFilterForm(forms.Form):
    blogger_discount = forms.IntegerField(
        required=False, label='Скидка блогера',
        widget=forms.TextInput(attrs={'placeholder': 'Введите процентную скидку блогера (число)'})
    )
    blogger_date = forms.ChoiceField(choices=DATE_CHOICES, required=False, label='Дата блогера')
