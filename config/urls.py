from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("agendamentos/", include("agendamentos.urls")),
    path("medicos/", include("medicos.urls")),
    path("pacientes/", include("pacientes.urls")),
    path("recepcao/", include("recepcao.urls")),
]