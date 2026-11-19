from django.core.exceptions import ValidationError


def validar_tamanho_arquivo(arquivo):
    limite = 1 * 1024 * 1024
    if arquivo.size > limite:
        raise ValidationError('A capa deve ter no máximo 1 MB.')
