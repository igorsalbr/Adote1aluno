from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# duvidas
from django.urls import reverse

# Create your models here.


class Eventos(models.Model):
    vestibular = 'Ves'
    simulado = 'Sim'
    outros = 'Out'
    CATEGORIAS = [
        (vestibular, 'Vestibular'),
        (simulado, 'Simulado'),
        (outros, 'Outros'),
    ]

    nome_ev = models.CharField(max_length=200)
    descr_ev = models.CharField(max_length=200, null=True, blank=True)
    data_ev = models.DateField()
    tipo_ev = models.CharField(
        max_length=3, choices=CATEGORIAS, default=simulado)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('calendario')

    def __str__(self):
        return self.nome_ev


class Simulado(models.Model):
    evento = models.OneToOneField(
        Eventos, on_delete=models.CASCADE, primary_key=True)

    progresso = 'Pro'
    encerrado = 'Enc'

    STATUS = [
        (progresso, 'Em progresso'),
        (encerrado, 'Encerrado'),
    ]

    url_sim = models.URLField(max_length=200)
    status_sim = models.CharField(
        max_length=3, choices=STATUS, default=progresso)

    def __str__(self):
        return self.evento.nome_ev

    def get_absolute_url(self):
        return reverse('simulado')


class Nota_simulados(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_simulado = models.ForeignKey(Simulado, on_delete=models.CASCADE)
    # nota é dada como um número racional de 0-100
    nota = models.FloatField(
        validators=[MaxValueValidator(100), MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id_user.first_name + ' ' + self.id_simulado.evento.nome_ev + ' ' + str(self.nota)

    def get_absolute_url(self):
        return reverse('atribuirnotas')


class Materia(models.Model):
    nome_mat = models.CharField(max_length=200)
    descr_mat = models.CharField(max_length=200, null=True, blank=True)
    id_user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_mat

    def get_absolute_url(self):
        return reverse('materia')


class Materiais(models.Model):
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    topico_mas = models.CharField(max_length=200)
    descr_mas = models.CharField(max_length=200, null=True, blank=True)
    data_mas = models.DateTimeField(auto_now=True)  # data da última edição

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, default=7)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.topico_mas

    def get_absolute_url(self):
        return reverse('materiais-detalhe', args=(self.id,))


class Arquivo_materiais(models.Model):
    id_materiais = models.ForeignKey(Materiais, on_delete=models.CASCADE)
    nome_arq = models.CharField(max_length=200, null=True, blank=True)
    file_mat = models.FileField(upload_to='materiais/', default="")
    is_active = models.BooleanField(default=True)


class Duvida(models.Model):
    aberto = 'Abe'
    encerrada = 'Enc'

    STATUS = [
        (aberto, 'Em aberto'),
        (encerrada, 'Encerrada'),
    ]

    topico_duv = models.CharField(max_length=200)
    texto = models.CharField(max_length=200, null=True, blank=True)
    file_duv = models.FileField(upload_to='duvidas/', null=True, blank=True)

    status_duv = models.CharField(max_length=3, choices=STATUS, default=aberto)
    data_duv = models.DateTimeField(auto_now=True)  # data da última edição
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.topico_duv

    def get_absolute_url(self):
        return reverse('duvidas-detalhe', args=(self.id,))


class Respostas(models.Model):
    id_duvida = models.ForeignKey(Duvida, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200, null=True, blank=True)
    file_res = models.FileField(
        upload_to='duvidas/', null=True, blank=True)

    data_res = models.DateTimeField(auto_now=True)  # data da última edição
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id_duvida.topico_duv

    def get_absolute_url(self):
        return reverse('duvidas-detalhe', args=(self.id_duvida.id,))

