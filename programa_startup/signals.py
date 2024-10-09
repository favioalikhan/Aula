from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Startup, IntegranteStartup, Modulo, ProgramaPage, Entregable

@receiver(post_save, sender=Startup)
def agregar_fundador_como_integrante(sender, instance, created, **kwargs):
    if created:
        IntegranteStartup.objects.create(
            usuario=instance.fundador,
            startup=instance,
            cargo='Founder',
            agregado_por=instance.fundador
        )
        

#Para guardar el id del programa en el modelo Modulo        
@receiver(post_save, sender=Modulo)
def set_programa_id(sender, instance, **kwargs):
    # Evitar recursión al comprobar si el campo ya tiene el valor correcto
    programa = instance.get_parent().specific
    if isinstance(programa, ProgramaPage) and instance.programa_id != programa.id:
        instance.programa_id = programa.id
        # Usa `update_fields` para evitar una nueva señal o bucle
        instance.save(update_fields=['programa_id'])
        
@receiver(post_save, sender=Entregable)
def update_startup_progress_on_create(sender, instance, **kwargs):
    # Actualizar el progreso de la startup cuando se crea un entregable
    if instance.startup:
        instance.startup.calcular_progreso()

@receiver(post_delete, sender=Entregable)
def update_startup_progress_on_delete(sender, instance, **kwargs):
    # Actualizar el progreso de la startup cuando se elimina un entregable
    if instance.startup:
        instance.startup.calcular_progreso()