# criar usuário
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
# criar dúvida
from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date
# TUDO ISSO AQUI É UM EXPERIMENTO DE INLINEFORMSETS
from django.forms.models import inlineformset_factory, BaseInlineFormSet

class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'id': 'senha', 'name': 'senha', 'placeholder': 'Nova senha'}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'id': 'repetirsenha', 'name': 'repetirsenha', 'placeholder': 'Repita sua nova senha'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                                        'id': 'username',
                                        'name': 'username',
                                        'placeholder': 'Nome de usuário'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                 'id': 'nome',
                                                 'name': 'nome',
                                                 'placeholder': 'Primeiro nome'}),
                'email': forms.EmailInput(attrs={'class': 'form-control form-control-user',
                                                 'id': 'email',
                                                 'name': 'email',
                                                 'placeholder': 'Endereço de email'}),
        }

class ChangeUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['first_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                 'id': 'nome',
                                                 'name': 'nome',
                                                 'placeholder': 'Primeiro nome'}),
                'email': forms.EmailInput(attrs={'class': 'form-control form-control-user',
                                                 'id': 'email',
                                                 'name': 'email',
                                                 'placeholder': 'Endereço de email'}),
        }

class TrocarSenhaForm(forms.Form):

    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'id': 'senha', 'name': 'senha', 'placeholder': 'Senha Atual'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'id': 'senhanova', 'name': 'senhanova', 'placeholder': 'Nova senha'}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'id': 'repetirsenha', 'name': 'repetirsenha', 'placeholder': 'Repita sua nova senha'}))

    class Meta:
        fields = ['password', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'id': 'username', 'name': 'username', 'placeholder': 'Nome de usuário'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'id': 'senha', 'name': 'senha', 'placeholder': 'Senha'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class AtualizarPermissoesForm(forms.Form):

    aluno = 'aluno'
    monitor = 'monitor'
    monitor_administrador = 'monitor_administrador'
    CATEGORIAS = [
        (aluno, 'Aluno'),
        (monitor, 'Monitor'),
        (monitor_administrador, 'Monitor Administrador'),
    ]

    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))

    grupo = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'grupo', 'name': 'grupo'}),
        choices=CATEGORIAS)

    class Meta:
        fields = ['user', 'grupo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update(
            {'class': 'form-control', 'id': 'usuario', 'required': True})


class CriarDuvidasForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ['topico_duv', 'texto', 'file_duv']

        widgets = {
            'topico_duv': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'topico',
                'name': 'topico',
                'placeholder': 'Tópico da sua dúvida'}),
            'texto': forms.Textarea(attrs={'class': 'form-control',
                                           'id': 'texto',
                                           'name': 'texto',
                                           'rows': '3',
                                           'placeholder': 'Descrição da sua dúvida'}),
            'file_duv': forms.FileInput(attrs={'class': 'form-control-file',
                                               'id': 'file',
                                               'name': 'file',
                                               'placeholder': 'Insira um arquivo'}),
        }


class EditarDuvidasForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ['topico_duv', 'texto', 'file_duv', 'status_duv']

        widgets = {
            'topico_duv': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'topico',
                'name': 'topico',
                'placeholder': 'Tópico da sua dúvida'}),
            'texto': forms.Textarea(attrs={'class': 'form-control',
                                           'id': 'texto',
                                           'name': 'texto',
                                           'rows': '3',
                                           'placeholder': 'Descrição da sua dúvida'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status_duv'].widget.attrs.update(
            {'class': 'form-control'})


class CriarEditarRespostasForm(forms.ModelForm):
    class Meta:
        model = Respostas
        fields = ['texto', 'file_res']

        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control',
                                           'id': 'texto',
                                           'name': 'texto',
                                           'rows': '3',
                                           'placeholder': 'Descrição da sua resposta'}),
        }


class CriarMateriaisForm(forms.ModelForm):

    files_mas = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file', 'id': 'files', 'name': 'files', 'multiple': True}), required=False)

    class Meta:
        model = Materiais
        fields = ['id_materia', 'topico_mas', 'descr_mas', 'files_mas']

        widgets = {
            'topico_mas': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'topico',
                'name': 'topico',
                'placeholder': 'Tópico do material'}),
            'descr_mas': forms.Textarea(attrs={'class': 'form-control',
                                               'id': 'descr',
                                               'name': 'descr',
                                               'rows': '3',
                                               'placeholder': 'Descrição do material'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_materia'].queryset = Materia.objects.filter(
            is_active=True)
        self.fields['id_materia'].widget.attrs.update(
            {'class': 'form-control', 'id': 'mat'})


class EditarMateriaisForm(forms.ModelForm):

    class Meta:
        model = Materiais
        fields = ['id_materia', 'topico_mas', 'descr_mas']  # , 'files_mas']

        widgets = {
            'topico_mas': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'topico',
                'name': 'topico',
                'placeholder': 'Tópico do material'}),
            'descr_mas': forms.Textarea(attrs={'class': 'form-control',
                                               'id': 'descr',
                                               'name': 'descr',
                                               'rows': '3',
                                               'placeholder': 'Descrição do material'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_materia'].queryset = Materia.objects.filter(
            is_active=True)
        self.fields['id_materia'].widget.attrs.update(
            {'class': 'form-control', 'id': 'mat'})


class CriarEditarMateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nome_mat', 'descr_mat', 'id_user']

        widgets = {
            'nome_mat': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'nome',
                'name': 'nome',
                'placeholder': 'Nome da matéria'}),
            'descr_mat': forms.Textarea(attrs={'class': 'form-control',
                                               'id': 'descr',
                                               'name': 'descr',
                                               'rows': '3',
                                               'placeholder': 'Descrição da matéria'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_user'].queryset = User.objects.filter(
            groups__name__contains='monitor', is_active=True)
        self.fields['id_user'].widget.attrs.update(
            {'class': 'form-control', 'id': 'resp'})



class ArquivosForm(forms.ModelForm):

    class Meta:
        model = Arquivo_materiais
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file_mat'].widget.attrs.update(
            {'class': 'form-control-file', 'id': 'file'})
        self.fields['nome_arq'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Insira o nome do arquivo', 'required': True})


ArquivosFormSet = inlineformset_factory(
    Materiais, Arquivo_materiais, form=ArquivosForm,
    fields=['nome_arq', 'file_mat', 'is_active'], extra=1)


class CriarEditarEventosForm(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['nome_ev', 'descr_ev', 'data_ev', 'tipo_ev']

        widgets = {
            'nome_ev': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'nome',
                'name': 'nome',
                'placeholder': 'Nome do evento'}),
            'descr_ev': forms.Textarea(attrs={'class': 'form-control',
                                              'id': 'descr',
                                              'name': 'descr',
                                              'rows': '3',
                                              'placeholder': 'Descrição do evento'}),
            'data_ev': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'data',
                'name': 'data',
                'min': date.today()}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_ev'].widget.attrs.update(
            {'class': 'form-control', 'id': 'tipo'})


class SimuladoForm(forms.ModelForm):

    class Meta:
        model = Simulado
        fields = ['url_sim', 'status_sim']

        widgets = {
            'url_sim': forms.URLInput(attrs={
                'class': 'form-control',
                'id': 'url',
                'name': 'url',
                'placeholder': 'Insira a url do simulado'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status_sim'].widget.attrs.update(
            {'class': 'form-control', 'id': 'status_sim'})


SimuladoFormSet = inlineformset_factory(
    Eventos, Simulado, form=SimuladoForm, extra=1, can_delete=False)

class AtribuirNotasForm(forms.ModelForm):

    class Meta:
        model = Nota_simulados
        fields = ['id_user', 'id_simulado', 'nota']

        widgets = {
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'nota',
                'name': 'nota',
                'step': 0.1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_user'].queryset = User.objects.filter(
            groups__name='aluno', is_active=True)
        self.fields['id_user'].widget.attrs.update(
            {'class': 'form-control', 'id': 'usuario'})
        self.fields['id_simulado'].queryset = Simulado.objects.filter(
            status_sim='Enc')
        self.fields['id_simulado'].widget.attrs.update(
            {'class': 'form-control', 'id': 'simulado'})

class EditarNotasForm(forms.ModelForm):

    class Meta:
        model = Nota_simulados
        fields = ['nota']

        widgets = {
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'nota',
                'name': 'nota',
                'step': 0.1}),
        }