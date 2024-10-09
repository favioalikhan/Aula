from django.db import models

# import parentalKey:
from modelcluster.fields import ParentalKey
# import FieldRowPanel and InlinePanel:
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)

# import DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin:
# import RichTextField
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)

# import AbstractEmailForm and AbstractFormField:
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

# import FormSubmissionsPanel:
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)


# import register_snippet:
from wagtail.snippets.models import register_snippet

# ... keep the definition of NavigationSettings and FooterText. Add FormField and FormPage:
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='Campos_formulario')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    Texto_gracias = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('Campos_formulario', label="Form fields"),
        FieldPanel('Texto_gracias'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

# ...keep the definition of the NavigationSettings model and add the FooterText model:
@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Texto Footer"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Texto Footer"

'''
BaseGenericSetting - clase de modelo base para definir un modelo de 
configuración que se aplica a todas las páginas web en lugar de solo a una página.
'''
@register_setting
class NavigationSettings(BaseGenericSetting):
    facebook_url = models.URLField(verbose_name="Facebook URL", blank=True)
    whatsapp_url = models.URLField(verbose_name="WhatsApp URL", blank=True)
    youtube_url = models.URLField(verbose_name="Youtube URL", blank=True)
    linkdln_url = models.URLField(verbose_name="Linkdln URL", blank=True)
    instagram_url = models.URLField(verbose_name="Instagram URL", blank=True)
    email_url = models.CharField(verbose_name="Correo URL", max_length=255, blank=True)
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook_url"),
                FieldPanel("whatsapp_url"),
                FieldPanel("youtube_url"),
                FieldPanel("linkdln_url"),
                FieldPanel("instagram_url"),
                FieldPanel("email_url"),
            ],
            "Configuración redes sociales",
        )
    ]