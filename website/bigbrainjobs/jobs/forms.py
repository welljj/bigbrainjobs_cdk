from django import forms


class SearchForm(forms.Form):
    what = forms.CharField(label_suffix="")
    where = forms.CharField(label_suffix="")

    what.widget.attrs.update({"class": "form-control", "placeholder": "keywords"})
    where.widget.attrs.update(
        {"class": "form-control", "placeholder": "city, state, zip"}
    )
