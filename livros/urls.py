from django.urls import path

from .views import (
    LivroCreateView,
    LivroDeleteView,
    LivroDetailView,
    LivroListView,
    LivroUpdateView,
    SobreView,
)

app_name = 'livros'

urlpatterns = [
    path('', LivroListView.as_view(), name='lista'),
    path('novo/', LivroCreateView.as_view(), name='criar'),
    path('<int:pk>/', LivroDetailView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', LivroUpdateView.as_view(), name='editar'),
    path('<int:pk>/excluir/', LivroDeleteView.as_view(), name='excluir'),
    path('sobre/', SobreView.as_view(), name='sobre'),
]
