from datetime import date

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.db import models

from .validators import validar_tamanho_arquivo


class Livro(models.Model):
    titulo = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, 'O título deve ter pelo menos 3 caracteres.')],
    )
    autor = models.CharField(max_length=150)
    ano_publicacao = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1450, 'O ano de publicação não pode ser anterior a 1450.'),
            MaxValueValidator(date.today().year, 'O ano de publicação não pode ser futuro.'),
        ],
    )
    paginas = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, 'Informe pelo menos 1 página.'),
            MaxValueValidator(5000, 'O livro pode ter no máximo 5000 páginas.'),
        ],
    )
    isbn = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{13}$', 'O ISBN deve conter exatamente 13 dígitos.')],
    )
    capa = models.ImageField(
        upload_to='capas/',
        blank=True,
        null=True,
        validators=[
            validar_tamanho_arquivo,
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
        ],
    )
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')

    def __str__(self):
        return self.titulo
