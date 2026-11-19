# Generated for the Django library project

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0003_livro_capa'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='disponivel',
            field=models.BooleanField(default=True, verbose_name='Disponível'),
        ),
    ]
