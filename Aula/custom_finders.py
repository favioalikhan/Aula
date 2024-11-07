from django.contrib.staticfiles.finders import AppDirectoriesFinder


class CustomAppDirectoriesFinder(AppDirectoriesFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo para la app "theme" revisando los nombres de las apps registradas
        self.apps = [app for app in self.apps if app == "theme"]
