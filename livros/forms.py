from django import forms

from .models import Livro


class LivroModelForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano_publicacao', 'paginas', 'isbn', 'capa', 'disponivel']
        labels = {
            'ano_publicacao': 'Ano de publicação',
            'paginas': 'Páginas',
            'isbn': 'ISBN',
            'capa': 'Capa do livro',
            'disponivel': 'Disponível para empréstimo',
        }
