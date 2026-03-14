from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_pacientes, name="lista_pacientes"),
    path("novo/", views.novo_paciente, name="novo_paciente"),
    path("<int:paciente_id>/editar/", views.editar_paciente, name="editar_paciente"),
    path("<int:paciente_id>/excluir/", views.excluir_paciente, name="excluir_paciente"),
]