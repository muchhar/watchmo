from django.apps import AppConfig


class WebscraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webscraper'

    def ready(self):
        from . import scheduler
        #import scheduler
        scheduler.start()