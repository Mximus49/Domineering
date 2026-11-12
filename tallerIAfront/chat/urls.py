"""
URLs de la app "chat".

Cada path() conecta una direccion del navegador con una funcion de views.py:
  http://127.0.0.1:8000/          -> views.chat
  http://127.0.0.1:8000/reiniciar/ -> views.reiniciar
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("reiniciar/", views.reiniciar, name="reiniciar"),
]
