from django.db import models
from django.db.models.sql.datastructures import Join
from django.db.models.sql.constants import LOUTER
import warnings
from .exceptions import PrefetchUnusedWarning


class QuerySet(models.QuerySet):
    def _fetch_all(self):
        super()._fetch_all()
        if self._result_cache is not None:
            # Get left joins in query alias_map
            related_alias_map = {
                structure.join_field.related_model
                for alias, structure in self.query.alias_map.items()
                if isinstance(structure, Join) and structure.join_type == LOUTER
            }
            # Filter
            unprefetched_fields = [
                field.name
                for field in self.model._meta.many_to_many
                if field.name not in self._prefetch_related_lookups
                and field.related_model in related_alias_map
            ]
            if unprefetched_fields:
                unprefetched_fields = ", ".join(unprefetched_fields)
                warnings.warn(
                    PrefetchUnusedWarning(f"Expected fields : {unprefetched_fields}")
                )
