from django.views.generic import TemplateView, ListView

from .models import Vinyl


class IndexView(ListView):
    template_name = 'vinyl/index.html'
    context_object_name = 'vinyls'

    def get_queryset(self):
        return Vinyl.objects.with_index_data().all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
