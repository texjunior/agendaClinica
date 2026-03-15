from django.urls import path
from . import views

urlpatterns = [
    path("emitir-senha/", views.emitir_senha, name="emitir_senha"),
    path("senha/<int:senha_id>/", views.senha_emitida, name="senha_emitida"),
    path("painel-senhas/", views.painel_senhas, name="painel_senhas"),
    path("guiche", views.guiche_atendimento, name="guiche_atendimento"),

    path("guiches/", views.lista_guiches, name="lista_guiches"),
    path("guiches/novo/", views.novo_guiche, name="novo_guiche"),
    path("guiches/<int:guiche_id>/editar/", views.editar_guiche, name="editar_guiche"),
    path("guiches/<int:guiche_id>/excluir/", views.excluir_guiche, name="excluir_guiche"),
]