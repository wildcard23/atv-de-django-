from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import LivroModelForm
from .models import Livro


class LivroListView(LoginRequiredMixin, ListView):
    model = Livro
    template_name = 'livros/lista.html'
    context_object_name = 'livros'
    ordering = ['titulo']

    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get('q', '').strip()
        if busca:
            queryset = queryset.filter(Q(titulo__icontains=busca) | Q(autor__icontains=busca))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busca'] = self.request.GET.get('q', '').strip()
        return context


class LivroDetailView(LoginRequiredMixin, DetailView):
    model = Livro
    template_name = 'livros/detalhe.html'
    context_object_name = 'livro'


class LivroCreateView(LoginRequiredMixin, CreateView):
    model = Livro
    form_class = LivroModelForm
    template_name = 'livros/formulario.html'
    success_url = reverse_lazy('livros:lista')
    extra_context = {'titulo': 'Cadastrar livro'}

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        return super().form_valid(form)


class LivroUpdateView(LoginRequiredMixin, UpdateView):
    model = Livro
    form_class = LivroModelForm
    template_name = 'livros/formulario.html'
    success_url = reverse_lazy('livros:lista')
    extra_context = {'titulo': 'Editar livro'}

    def get_queryset(self):
        return super().get_queryset().filter(registered_by=self.request.user)


class LivroDeleteView(LoginRequiredMixin, DeleteView):
    model = Livro
    template_name = 'livros/livro_confirm_delete.html'
    context_object_name = 'livro'
    success_url = reverse_lazy('livros:lista')

    def get_queryset(self):
        return super().get_queryset().filter(registered_by=self.request.user)


class SobreView(LoginRequiredMixin, TemplateView):
    template_name = 'livros/sobre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_livros'] = Livro.objects.count()
        context['livros_disponiveis'] = Livro.objects.filter(disponivel=True).count()
        return context
