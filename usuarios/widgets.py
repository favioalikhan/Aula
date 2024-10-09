from django import forms

class CustomProfileImageWidget(forms.ClearableFileInput):
    template_name = "custom_widgets/profile_image.html"  # Ruta del template que usarás
    
class CustomStartupImageWidget(forms.ClearableFileInput):
    template_name = "custom_widgets/startup_image.html"  # Ruta del template que usarás
