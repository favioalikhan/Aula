from django.core.management.base import BaseCommand
from usuarios.models import CustomUser
from django.db import models

class Command(BaseCommand):
    help = 'Eliminar usuarios duplicados por email'

    def handle(self, *args, **kwargs):
        duplicated_emails = CustomUser.objects.values('email').annotate(count=models.Count('id')).filter(count__gt=1)
        
        for email in duplicated_emails:
            users = CustomUser.objects.filter(email=email['email'])
            users.exclude(id=users.first().id).delete()

        self.stdout.write(self.style.SUCCESS('Usuarios duplicados eliminados'))
