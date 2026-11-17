from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from app_escolar_backend.views import auth
from app_escolar_backend.views import users
#from app_escolar_backend.views import maestros
#from app_escolar_backend.views import alumnos

urlpatterns = [
    # Crear Administrador
    path('admin/', users.AdminView.as_view()),
    # Login
    path('login/', auth.CustomAuthToken.as_view()),
    # logout
    path('logout/', auth.Logout.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
