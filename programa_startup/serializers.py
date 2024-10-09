from rest_framework import serializers
from .models import Tarea, Entregable, Sesion, Startup

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class StartupProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = '__all__'

class EntregableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entregable
        fields = '__all__'
