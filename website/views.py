from django.shortcuts import render, redirect

# MODELS: importa os modelos criados em models.py
from .models import *

# FORMS: importa os formulários criados em forms.py
from .forms import *

# LOGIN
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.urls import reverse_lazy

# AUTENTICAÇÃO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# LISTVIEW:
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.db import transaction
from datetime import date

# VIEWS PÚBLICAS
# Quem somos


def quemsomos(request):
    return render(request, 'quemsomos.html', {})


@login_required(login_url='login')
def atualizarpermissoes(request):
    context = {}
    if request.method == "POST":
        form = AtualizarPermissoesForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            nome_grupo = form.cleaned_data.get('grupo')
            grupo = Group.objects.get(name=nome_grupo)
            user.groups.clear()
            user.groups.add(grupo)
            if nome_grupo == 'monitor_administrador':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False

            user.save()

            return redirect('atualizarpermissoes')
    else:
        form = AtualizarPermissoesForm()
        context = {'form': form}
    return render(request, 'atualizarpermissoes.html', context)

# Calendário


def calendario(request):
    context = {
        'eventos_cal': Eventos.objects.filter(data_ev__gte=date.today(), is_active=True).order_by('data_ev')
    }
    return render(request, 'calendario.html', context)


class CriarEventosView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Eventos
    form_class = CriarEditarEventosForm
    template_name = 'eventos_criar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['simulado'] = SimuladoFormSet(self.request.POST)
        else:
            context['simulado'] = SimuladoFormSet()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)  # salva o forms

        if form.instance.tipo_ev == 'Sim':
            context = self.get_context_data()
            simulado = context['simulado']
            # cria o objeto Simulado a partir do inline Formset
            for sim in simulado:
                if sim.is_valid():
                    sim.instance.evento = self.object
                    sim.save()

        # retorna
        return response


class EventosDetailView(DetailView):
    template_name = 'eventos_detalhe.html'

    def get_queryset(self):
        return Eventos.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.tipo_ev == 'Sim':
            context['simulado'] = Simulado.objects.get(evento=self.object.pk)
        return context


class EditarEventosView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = CriarEditarEventosForm
    template_name = 'eventos_editar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['simulado'] = SimuladoFormSet(
                self.request.POST, instance=self.object)
        else:
            context['simulado'] = SimuladoFormSet(
                instance=self.object)
        return context

    def form_valid(self, form):
        evento = Eventos.objects.get(pk=self.object.id)
        if form.instance.tipo_ev == 'Sim':
            context = self.get_context_data()
            simulado = context['simulado']
            with transaction.atomic():
                for sim in simulado:
                    if sim.is_valid() and sim.has_changed():
                        sim.instance.evento = self.object
                        sim.save()
        else:
            if evento.tipo_ev == 'Sim':
                simulado = Simulado.objects.get(evento=evento)
                simulado.delete()

        return super().form_valid(form)

    def get_queryset(self):
        return Eventos.objects.filter(is_active=True)

# Eventos: Excluir


def eventosexcluir(request, pk):
    if request.user.groups.all()[0].name == 'monitor_administrador':
        Eventos.objects.filter(id=pk).update(is_active=False)
    return redirect('calendario')


# Simulado: Visualizar


class SimuladoView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'simulado.html'

    def get_queryset(self):
        return Simulado.objects.filter(evento__data_ev__gte=date.today(), evento__is_active=True)

    ordering = ['-evento.data_ev']

# Simulado: Visualizar Aluno


class SimuladoAlunoView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'acessar_simulado.html'

    def get_queryset(self):
        aluno = self.request.user
        return Simulado.objects.filter(evento__data_ev__gte=aluno.date_joined.date(), evento__is_active=True)

    ordering = ['-evento.data_ev']

# Simulado: Editar


class EditarSimuladoView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = SimuladoForm
    model = Simulado
    template_name = 'simulado_editar.html'

# Nota_simulados: Visualizar


class NotasView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'notas.html'

    def get_queryset(self):
        return Nota_simulados.objects.filter(is_active=True)

    ordering = ['-id_simulado.evento.data_ev']

# Nota_simulados: Visualizar

class NotasAlunoView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'notas_aluno.html'

    def get_queryset(self):
        return Nota_simulados.objects.filter(id_user=self.request.user, is_active=True)

    ordering = ['-id_simulado.evento.data_ev']

# Nota_simulados: Criar


class AtribuirNotasView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Nota_simulados
    form_class = AtribuirNotasForm
    template_name = 'atribuirnotas.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data['id_user']
            simulado = form.cleaned_data['id_simulado']
            if not Nota_simulados.objects.filter(id_user=user, id_simulado=simulado, is_active=True).exists():
                nota = form.save()
                nota.save()
                return redirect('atribuirnotas')

        return render(request, self.template_name, {'form': form})

# Nota_simulados: Editar


class EditarNotasView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = EditarNotasForm
    template_name = 'editarnotas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nota_sim'] = Nota_simulados.objects.get(id=self.object.pk)
        return context

    def get_queryset(self):
        return Nota_simulados.objects.filter(is_active=True)

# Nota_simulados: Excluir


@login_required(login_url='login')
def excluirnotas(request, pk):
    if request.user.groups.all()[0].name != 'aluno':
        Nota_simulados.objects.filter(id=pk).update(is_active=False)
    return redirect('notas')

# Login


class UsuarioView(LoginView):
    model = User
    form_class = LoginUserForm
    template_name = 'login.html'

# Perfil


class PerfilUsuarioView(LoginRequiredMixin, UpdateView):
    form_class = ChangeUserForm
    template_name = 'perfil.html'
    success_url = reverse_lazy('login')

    def get_queryset(self):
        return User.objects.filter(is_active=True)

# Excluir usuário


@login_required(login_url='login')
def userexcluir(request, pk):
    if User.objects.get(id=pk) == request.user:
        User.objects.filter(id=pk).update(is_active=False)
    return redirect('login')

# Trocar senha


def trocarsenha(request):
    if request.method == "POST":
        form = TrocarSenhaForm(request.POST)
        if form.is_valid() and request.user.check_password(form.cleaned_data['password']):
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                u = User.objects.get(pk=request.user.id)
                u.set_password(password1)
                u.save()
        return redirect('logout')
    else:
        form = TrocarSenhaForm()
        context = {'form': form}
    return render(request, 'trocar_senha.html', context)

# Logout


class AnonimoView(LogoutView):
    model = User
    template_name = 'logout.html'

# Cadastro


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            uid = User.objects.get(username=form.cleaned_data.get('username'))
            group = Group.objects.get(name='aluno')
            uid.groups.add(group)

            return redirect('login')
        else:
            context = {'form': form}
            return render(request, 'register.html', context)
    else:
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context)

# Esqueci minha senha


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        query = User.objects.filter(username=username)
        if query.exists():
            user = query[0]
            newpassword = User.objects.make_random_password(10)
            user.set_password(newpassword)
            user.save()
            message_name = 'Recuperação de Senha Adote um Aluno'
            message = 'Você realizou o pedido de uma alteração de senha. Sua nova senha é: ' + \
                newpassword + ' Tome mais cuidado!'
            message_email = 'adoteumalunopoli@gmail.com'
            recipient = user.email

            send_mail(
                message_name,
                message,
                message_email,
                [recipient],
            )
        return redirect('login')

    else:
        return render(request, 'forgot-password.html', {})



def index(request):
    return render(request, 'index.html', {})

# VIEWS QUE EXIGEM AUTENTICAÇÃO
# Home / Index
# Duvidas: Visualizar em aberto


class DuvidasView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'duvidas.html'

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == 'aluno':
            return Duvida.objects.filter(id_user=self.request.user, status_duv='Abe', is_active=True)

        else:
            return Duvida.objects.filter(status_duv='Abe', is_active=True)

    ordering = ['-id']

# Duvidas: Visualizar encerradas


class DuvidasEncView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'duvidas_encerradas.html'

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == 'aluno':
            return Duvida.objects.filter(id_user=self.request.user, status_duv='Enc', is_active=True)

        else:
            return Duvida.objects.filter(status_duv='Enc', is_active=True)

    ordering = ['-id']

# Duvidas: Detalhes


class DuvidasDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    template_name = 'duvidas_detalhe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['respostas'] = Respostas.objects.filter(
            id_duvida=self.object.pk, is_active=True)
        return context

    def get_queryset(self):
        return Duvida.objects.filter(is_active=True)

# Duvidas: Criar


class CriarDuvidasView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Duvida
    form_class = CriarDuvidasForm
    template_name = 'duvidas_criar.html'

    def form_valid(self, form):
        form.instance.id_user = self.request.user
        return super().form_valid(form)

# Duvidas: Editar


class DuvidasEditarView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = EditarDuvidasForm
    template_name = 'duvidas_editar.html'

    def get_queryset(self):
        return Duvida.objects.filter(is_active=True)

# Duvidas: Excluir


def duvidasexcluir(request, pk):
    if (request.user.groups.all()[0].name == 'aluno' and Duvida.objects.get(id=pk).id_user.id == request.user.id) or request.user.groups.all()[0].name != 'aluno':
        Duvida.objects.filter(id=pk).update(is_active=False)
    return redirect('duvidas')


# Respostas: Criar


class CriarRespostasView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Respostas
    form_class = CriarEditarRespostasForm
    template_name = 'respostas_criar.html'

    def form_valid(self, form):
        form.instance.id_user = self.request.user
        form.instance.id_duvida = Duvida.objects.get(id=self.kwargs['pkduv'])
        return super().form_valid(form)

# Respostas: Editar


class RespostasEditarView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = CriarEditarRespostasForm
    template_name = 'respostas_editar.html'

    def get_queryset(self):
        return Respostas.objects.filter(is_active=True)


# Respostas: Excluir


def respostasexcluir(request, pk):
    resposta = Respostas.objects.get(id=pk)
    if resposta.id_user.id == request.user.id:
        resposta.is_active = False
        resposta.save()

    return redirect('duvidas-detalhe', pk=resposta.id_duvida.id)


# Materiais: Visualizar


class MateriaisView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'materiais.html'

    def get_queryset(self):
        return Materiais.objects.filter(id_materia__is_active=True, is_active=True)

    ordering = ['-id']

# Materiais: Detalhes


class MateriaisDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    template_name = 'materiais_detalhe.html'

    def get_queryset(self):
        return Materiais.objects.filter(id_materia__is_active=True, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['arquivos'] = Arquivo_materiais.objects.filter(
            id_materiais=self.object.pk, is_active=True)
        return context

# Materiais: Criar


class CriarMateriaisView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Materiais
    form_class = CriarMateriaisForm
    template_name = 'materiais_criar.html'

    def form_valid(self, form):
        form.instance.id_user = self.request.user  # atualiza o usuário
        response = super().form_valid(form)  # salva o forms

        # cria o objeto Arquivos_materiais a partir dos uploads
        files = self.request.FILES.getlist('files_mas')
        for f in files:
            instance = Arquivo_materiais(
                id_materiais=self.object, file_mat=f, nome_arq=f.name)
            instance.save()

        # retorna
        return response


# Materiais: Editar


class MateriaisEditarView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = EditarMateriaisForm
    template_name = 'materiais_editar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['arquivo_materiais'] = ArquivosFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['arquivo_materiais'] = ArquivosFormSet(
                instance=self.object, queryset=Arquivo_materiais.objects.filter(is_active=True))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        arquivos = context['arquivo_materiais']
        form.instance.id_user = self.request.user  # atualiza o usuário
        with transaction.atomic():
            self.object = form.save()
            for arq in arquivos:
                if arq.is_valid() and arq.has_changed():
                    if arq.cleaned_data['nome_arq'] == None:
                        instance = arq.save(commit=False)
                        instance.nome_arq = arq.cleaned_data['file_mat']
                        instance.save()
                    else:
                        arq.save()

        return super().form_valid(form)

    def get_queryset(self):
        return Materiais.objects.filter(id_materia__is_active=True, is_active=True)

# Materiais: Excluir


def materiaisexcluir(request, pk):
    if request.user.groups.all()[0].name != 'aluno':
        Materiais.objects.filter(id=pk).update(is_active=False)
    return redirect('materiais')


# Materia: Visualizar


class MateriaView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'materia.html'

    def get_queryset(self):
        return Materia.objects.filter(is_active=True)

    ordering = ['-id']


# Materia: Criar


class CriarMateriaView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Materia
    form_class = CriarEditarMateriaForm  # usamos o mesmo forms por conveniência
    template_name = 'materia_criar.html'

# Materia: Editar


class MateriaEditarView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = CriarEditarMateriaForm  # usamos o mesmo forms por conveniência
    template_name = 'materia_editar.html'

    def get_queryset(self):
        return Materia.objects.filter(is_active=True)

# Materia: Excluir


def materiaexcluir(request, pk):
    if request.user.groups.all()[0].name == 'monitor_administrador':
        Materia.objects.filter(id=pk).update(is_active=False)
    return redirect('materia')
