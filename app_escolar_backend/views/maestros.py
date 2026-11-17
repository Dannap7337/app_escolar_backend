import json
from django.db.models import *
from django.db import transaction
from app_escolar_backend.serializers import *
from app_escolar_backend.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group

class MaestrosView(generics.CreateAPIView):

    # Permisos por metodo (sobrescribe el comportamiento default)
    # Verifica que el usuario este autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return[] #POST no requiere autenticacion

    @transaction.atomic
    def post(self, request, *args, **kwargs):


        # Serializamos los datos de autentificacion del Maestro para volverlo de nuevo JSON
        user = UserSerializer(data=request.data)
        if user.is_valid():
            #Grabar datos del usuario --- esto va en la tabla authUser
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']

            # Valida si existe el usuario o el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Usuario "+email+", ya esta registrado"},400)

            # Función para mandar a registrar a la BD
            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)

            # Sentencia para mandar a guardar a la BD
            user.save()
            # Cifrar la contraseña
            user.set_password(password)
            # Volver a guardar
            user.save()

            # Se guardan en la base de datos el tipo de rol
            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            # Almacenar los datos adicionales del maestro
            maestro = Maestros.objects.create(user=user,
                                                   id_trabajador= request.data["id_trabajador"],
                                                   fecha_nacimiento= request.data["fecha_nacimiento"],
                                                   telefono= request.data["telefono"],
                                                   curp= request.data["curp"].upper(),
                                                   rfc= request.data["rfc"].upper(),
                                                   cubiculo= request.data["cubiculo"],
                                                   area_investigacion= request.data["area_investigacion"],
                                                   materias_array= json.dumps(request.data["materias"]))
            maestro.save()
            
            return Response({"Alumno creado correctamente": maestro.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
