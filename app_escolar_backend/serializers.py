from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

# Este serializer tiene los datos de autenticacion de cualquier usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")

# Definimos serialiser para administradores
class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        field = '__all__'

# Definimos serialiser para maestros
class MaestrosSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        field = '__all__'

# TODO: Agregar serializers para alumnos