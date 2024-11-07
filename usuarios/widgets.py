from django.forms.widgets import (
    ClearableFileInput,
    FILE_INPUT_CONTRADICTION,
    CheckboxInput,
)
from django.utils.translation import gettext_lazy as _


class CustomProfileImageWidget(ClearableFileInput):
    template_name = "custom_widgets/profile_image.html"  # Ruta del template que usarás
    clear_checkbox_label = _("Eliminar")
    initial_text = _("Imagen actual")
    input_text = _("Cambiar imagen")

    def clear_checkbox_name(self, name):
        return name + "-clear"

    def clear_checkbox_id(self, name):
        return name + "_clear_id"

    def value_from_datadict(self, data, files, name):
        upload = files.get(name)
        clear_checkbox_name = self.clear_checkbox_name(name)
        is_clear = CheckboxInput().value_from_datadict(data, files, clear_checkbox_name)
        if not self.is_required and is_clear:
            if upload:
                return FILE_INPUT_CONTRADICTION
            return False  # Señal para eliminar el archivo
        return upload


class CustomStartupImageWidget(ClearableFileInput):
    template_name = "custom_widgets/startup_image.html"  # Ruta del template que usarás
    clear_checkbox_label = _("Eliminar")
    initial_text = _("Imagen actual")
    input_text = _("Cambiar imagen")

    def clear_checkbox_name(self, name):
        return name + "-clear"

    def clear_checkbox_id(self, name):
        return name + "_clear_id"

    def value_from_datadict(self, data, files, name):
        upload = files.get(name)
        clear_checkbox_name = self.clear_checkbox_name(name)
        is_clear = CheckboxInput().value_from_datadict(data, files, clear_checkbox_name)
        if not self.is_required and is_clear:
            if upload:
                return FILE_INPUT_CONTRADICTION
            return False  # Señal para eliminar el archivo existente
        return upload
