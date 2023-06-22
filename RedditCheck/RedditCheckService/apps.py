from django.apps import AppConfig


class RedditcheckserviceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "RedditCheckService"
    verbose_name="RedditCheck Menu "

    def ready(self):
        from jobs import updater
        updater.start()
