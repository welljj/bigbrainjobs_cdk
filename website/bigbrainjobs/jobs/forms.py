from django import forms


class SearchForm(forms.Form):
    what = forms.CharField()
    where = forms.CharField()
