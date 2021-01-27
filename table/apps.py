from django.apps import AppConfig


class TableConfig(AppConfig):
    name = 'table'

    def ready(self):
        try:
            from table import signals
        except ImportError:
            pass
