# Mini Biblioteca — Django

Projeto Django para cadastro, listagem, detalhe, edição e exclusão de livros.

## Recursos

- Class-Based Views
- Validação de campos
- Upload de capa
- PostgreSQL com credenciais em `.env`
- PostgreSQL não incluído no repositório

## Configuração

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```
