from django.db import models


class VinylManager(models.Manager):
    def with_index_data(self):
        return self.prefetch_related('images') \
            .prefetch_related('tags') \
            .select_related('discount')
