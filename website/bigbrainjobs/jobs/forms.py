from django import forms


class SearchForm(forms.Form):
    what = forms.CharField(label_suffix="", label="What: job title, keywords, company")
    where = forms.CharField(label_suffix="", label="Where: city, state, zip")

    what.widget.attrs.update(
        {"class": "form-control", "placeholder": "job title, keywords, company"}
    )
    where.widget.attrs.update(
        {"class": "form-control", "placeholder": "city, state, zip"}
    )
