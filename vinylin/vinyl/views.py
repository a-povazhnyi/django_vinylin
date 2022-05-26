from django.views.generic import ListView, DetailView

from .models import Vinyl


class IndexView(ListView):
    template_name = 'vinyl/index.html'
    context_object_name = 'vinyls'

    def get_queryset(self):
        return Vinyl.objects.with_index_data().all().order_by('id')


class VinylDetailView(DetailView):
    template_name = 'vinyl/single.html'

    def get_queryset(self):
        return Vinyl.objects.with_all_data().filter(pk=self.kwargs.get('pk'))
