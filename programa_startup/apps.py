from django.apps import AppConfig


class ProgramaStartupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'programa_startup'
    
    def ready(self):
        import programa_startup.signals 