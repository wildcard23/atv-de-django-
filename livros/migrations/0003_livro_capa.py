# Generated for the Django library project

from django.db import migrations, models
import livros.validators
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0002_validadores_livro'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='capa',
            field=models.ImageField(blank=True, null=True, upload_to='capas/', validators=[livros.validators.validar_tamanho_arquivo, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
    ]
