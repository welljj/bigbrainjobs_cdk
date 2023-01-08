from django.views.generic import FormView, ListView
from django.views.generic.edit import FormMixin
from .forms import SearchForm
from .models import Job


class Home(FormMixin, ListView):
    template_name = "home.html"
    form_class = SearchForm
    model = Job
    paginate_by = 10

    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset
        queryset = super().get_queryset()
        # Get the q GET parameter
        q = self.request.GET.get("what")
        location = self.request.GET.get("where")
        if q:
            # Return a filtered queryset
            return queryset.filter(title__icontains=q)
        # Return the base queryset
        return queryset
