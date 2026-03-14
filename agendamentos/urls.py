from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_agendamentos, name="lista_agendamentos"),
    path("novo/", views.novo_agendamento, name="novo_agendamento"),
    path("<int:agendamento_id>/editar/", views.editar_agendamento, name="editar_agendamento"),
    path("<int:agendamento_id>/cancelar/", views.cancelar_agendamento, name="cancelar_agendamento"),
    path("horarios-disponiveis/", views.horarios_disponiveis, name="horarios_disponiveis"),
    path("convenios-do-medico/", views.convenios_do_medico, name="convenios_do_medico"),
]