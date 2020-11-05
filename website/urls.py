from django.urls import path
from . import views

# DUVIDAS
from .views import *

# LOGIN
from .views import UsuarioView, AnonimoView

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),

    path('calendario', views.calendario, name="calendario"),
    path('quemsomos', views.quemsomos, name="quemsomos"),
    path('atualizarpermissoes', views.atualizarpermissoes, name="atualizarpermissoes"),

    # URL: eventos - detalhe
    path('eventos/<int:pk>/', EventosDetailView.as_view(), name="eventos-detalhe"),

    # URL: eventos - criar
    path('eventos/criar', CriarEventosView.as_view(), name="eventos-criar"),

    # URL: eventos - editar
    path('eventos/editar/<int:pk>/',
         EditarEventosView.as_view(), name="eventos-editar"),
    # URL: eventos - excluir
    path('eventos/excluir/<int:pk>/',
         views.eventosexcluir, name="eventos-excluir"),
    # URL: simulado - visualizar
    path('simulado', SimuladoView.as_view(), name="simulado"),
    # URL: simulado - visualizar
    path('simulado/alunos', SimuladoAlunoView.as_view(), name="simulado-alunos"),
    # URL: simulado - editar
    path('simulado/editar/<int:pk>/',
         EditarSimuladoView.as_view(), name="simulado-editar"),
    # URL: nota_simulados - visualizar
    path('notas',
         NotasView.as_view(), name="notas"),
    # URL: nota_simulados - visualizar
    path('notas/aluno',
         NotasAlunoView.as_view(), name="notas-aluno"),
    # URL: nota_simulados - criar
    path('notas/atribuir',
         AtribuirNotasView.as_view(), name="atribuirnotas"),
    # URL: nota_simulados - editar
    path('notas/editar/<int:pk>/',
         EditarNotasView.as_view(), name="editarnotas"),
    # URL: nota_simulados - excluir
    path('notas/excluir/<int:pk>/',
         views.excluirnotas, name="excluirnotas"),

    # URL: views - autenticação de usuário:
    path('login', UsuarioView.as_view(),
         name="login"),  # extends base_registration
    path('logout', AnonimoView.as_view(), name="logout"),
    path('register', views.register, name="register"),
    path('forgot-password', views.forgot_password, name="forgot-password"),
    path('perfil/<int:pk>/', PerfilUsuarioView.as_view(), name="perfil"),
    path('trocarsenha', views.trocarsenha, name="trocarsenha"),
    path('excluirusuario/<int:pk>/', views.userexcluir, name="excluirusuario"),

    # URL: duvidas - visualizar
    path('duvidas', DuvidasView.as_view(), name="duvidas"),
    path('duvidasencerradas', DuvidasEncView.as_view(), name="duvidas-encerradas"),

    # URL: duvidas - detalhe
    path('duvidas/<int:pk>/', DuvidasDetailView.as_view(), name="duvidas-detalhe"),
    # URL: duvidas - criar
    path('duvidas/criar', CriarDuvidasView.as_view(), name="duvidas-criar"),
    # URL: duvidas - editar
    path('duvidas/editar/<int:pk>/',
         DuvidasEditarView.as_view(), name="duvidas-editar"),
    # URL: duvidas - excluir
    path('duvidas/excluir/<int:pk>/',
         views.duvidasexcluir, name="duvidas-excluir"),

    # URL: respostas - criar
    path('duvidas/<int:pkduv>/responder/',
         CriarRespostasView.as_view(), name="respostas-criar"),

    # URL: respostas - editar
    path('respostas/editar/<int:pk>/',
         RespostasEditarView.as_view(), name="respostas-editar"),

    # URL: respostas - excluir
    path('respostas/excluir/<int:pk>/',
         views.respostasexcluir, name="respostas-excluir"),

    # URL: materiais - visualizar
    path('materiais', MateriaisView.as_view(), name="materiais"),

    # URL: materiais - detalhe
    path('materiais/<int:pk>/', MateriaisDetailView.as_view(),
         name="materiais-detalhe"),
    # URL: materiais - criar
    path('materiais/criar', CriarMateriaisView.as_view(), name="materiais-criar"),

    # URL: materiais - editar
    path('materiais/editar/<int:pk>/',
         MateriaisEditarView.as_view(), name="materiais-editar"),

    # URL: materiais - excluir
    path('materiais/excluir/<int:pk>/',
         views.materiaisexcluir, name="materiais-excluir"),

    # URL: materia - visualizar
    path('materia', MateriaView.as_view(), name="materia"),

    # URL: materia - criar
    path('materia/criar', CriarMateriaView.as_view(), name="materia-criar"),

    # URL: materia - editar
    path('materia/editar/<int:pk>/',
         MateriaEditarView.as_view(), name="materia-editar"),
    # URL: materia - excluir
    path('materia/excluir/<int:pk>/',
         views.materiaexcluir, name="materia-excluir"),
]

'''
    teste não funciona, tá aí só pra salvar a configuração da navbar de usuário anônimo / calendário igual
    login não foi parametrizado com django forms (estático), só tem mensagens de erro
    verificar funcionalidades da página register
    forgot-password completamente estático
    duvidas fizemos o visualizar, detalhes e adicionar (falta editar, responder e excluir)
    quemsomos falta conteúdo

'''
