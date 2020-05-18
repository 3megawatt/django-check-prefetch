from django.apps import AppConfig


class AppConfig(AppConfig):
    name = "app"

    def get_models(self, include_auto_created=False, include_swapped=False):
        self.apps.check_models_ready()
        for model in self.models.values():
            if model._meta.auto_created and not include_auto_created:
                continue
            if model._meta.swapped and not include_swapped:
                continue
            from check_prefetch import Model

            if Model not in getattr(model, "__mro__"):
                mro_list = list(getattr(model, "__mro__"))
                mro_list.insert(1, Model)
                model = type(model.__name__, tuple(mro_list), dict(vars(model)))
            yield model
