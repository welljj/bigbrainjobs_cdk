from django.views.generic import FormView
from .forms import SearchForm


class Home(FormView):
    template_name: str = "home.html"
    form_class = SearchForm
    success_url = "/results/"
