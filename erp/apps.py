from django.apps import AppConfig


class ErpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'erp'

    def ready(self) -> None:
        import erp.signals  # noqa: F401
        return super().ready()
