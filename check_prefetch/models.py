from .query import QuerySet
from django.db import models

Manager = models.Manager.from_queryset(QuerySet)


class Model(models.Model):

    objects = Manager()
    check_prefetch_manager = Manager()

    class Meta:
        abstract = True
        base_manager_name = "check_prefetch_manager"
