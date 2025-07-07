from django.apps import AppConfig


class ExecutionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'execution'

    def ready(self):
        import execution.signals  # À adapter avec le nom de ton app

