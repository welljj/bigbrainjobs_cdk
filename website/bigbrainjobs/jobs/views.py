from django.views.generic import FormView
from .forms import SearchForm


class Home(FormView):
    template_name = "home.html"
    form_class = SearchForm
