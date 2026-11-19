# Generated for the Django library project

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livro',
            old_name='ano',
            new_name='ano_publicacao',
        ),
        migrations.AlterField(
            model_name='livro',
            name='titulo',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(3, 'O título deve ter pelo menos 3 caracteres.')]),
        ),
        migrations.AlterField(
            model_name='livro',
            name='ano_publicacao',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1450, 'O ano de publicação não pode ser anterior a 1450.'), django.core.validators.MaxValueValidator(2026, 'O ano de publicação não pode ser futuro.')]),
        ),
        migrations.AddField(
            model_name='livro',
            name='paginas',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1, 'Informe pelo menos 1 página.'), django.core.validators.MaxValueValidator(5000, 'O livro pode ter no máximo 5000 páginas.')]),
        ),
        migrations.AddField(
            model_name='livro',
            name='isbn',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator('^\\d{13}$', 'O ISBN deve conter exatamente 13 dígitos.')]),
        ),
    ]
