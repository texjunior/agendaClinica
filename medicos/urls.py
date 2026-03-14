from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_medicos, name="lista_medicos"),
    path("novo/", views.novo_medico, name="novo_medico"),
    path("<int:medico_id>/editar/", views.editar_medico, name="editar_medico"),
    path("<int:medico_id>/excluir/", views.excluir_medico, name="excluir_medico"),

    path("especialidades/", views.lista_especialidades, name="lista_especialidades"),
    path("especialidades/nova/", views.nova_especialidade, name="nova_especialidade"),
    path("especialidades/<int:especialidade_id>/editar/", views.editar_especialidade, name="editar_especialidade"),
    path("especialidades/<int:especialidade_id>/excluir/", views.excluir_especialidade, name="excluir_especialidade"),

    path("convenios/", views.lista_convenios, name="lista_convenios"),
    path("convenios/novo/", views.novo_convenio, name="novo_convenio"),
    path("convenios/<int:convenio_id>/editar/", views.editar_convenio, name="editar_convenio"),
    path("convenios/<int:convenio_id>/excluir/", views.excluir_convenio, name="excluir_convenio"),

    path("agendas/", views.lista_agendas_medicas, name="lista_agendas_medicas"),
    path("agendas/nova/", views.nova_agenda_medica, name="nova_agenda_medica"),
    path("agendas/<int:agenda_id>/editar/", views.editar_agenda_medica, name="editar_agenda_medica"),
    path("agendas/<int:agenda_id>/excluir/", views.excluir_agenda_medica, name="excluir_agenda_medica"),
    path("agendas/semanal/nova/", views.nova_agenda_semanal_medica, name="nova_agenda_semanal_medica"),
    path("agendas/semanal/dados/", views.agenda_semanal_do_medico, name="agenda_semanal_do_medico"),
]