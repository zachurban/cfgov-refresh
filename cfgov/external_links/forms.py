from django import forms


class ExternalLinksForm(forms.Form):
    url = forms.CharField(
        required=True,
        widget=forms.TextInput()
    )
