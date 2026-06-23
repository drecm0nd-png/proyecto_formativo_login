"""
URL configuration for proyecto1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# proyecto1/urls.py
# proyecto1/urls.py
from django.contrib import admin
from django.urls import path
from usuarios_app import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.mostrar_pagina_inicio, name='inicio'),
    path('registrar-producto/', views.registrar_producto, name='registrar_producto'),
    path('ver-productos/', views.ver_productos, name='ver_productos'),
    path('alterar-producto/<int:producto_id>/', views.alterar_producto, name='alterar_producto'),
    path('constituir-ingredientes/<int:producto_id>/', views.constituir_ingredients, name='constituir_ingredientes'),

    path('registrar-ingrediente/', views.registrar_ingrediente, name='registrar_ingrediente'),
    path('ver-ingredients/', views.ver_ingredientes, name='ver_ingredientes'),
    path('alterar-ingrediente/<int:ingrediente_id>/', views.alterar_ingrediente, name='alterar_ingrediente'),
    path('producto/cambiar-imagen/<int:producto_id>/', views.cambiar_imagen_producto, name='cambiar_imagen_producto'),
    

    path('registro/', views.registro, name='registro'),
    path('login/', views.inicio_sesion, name='inicio_sesion'),
    path('restablecer-contrasena/', views.restablecer_contrasena, name='restablecer_contrasena'),
    

    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'), # Y esta también
]