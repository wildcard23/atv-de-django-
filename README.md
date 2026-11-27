# Mini Biblioteca — Django

Projeto Django para cadastro, listagem, detalhe, edição e exclusão de livros.

## Recursos

- Class-Based Views
- Validação de campos
- Upload de capa
- Cadastro e login com e-mail
- Acervo protegido e edição/exclusão restrita ao responsável pelo cadastro
- PostgreSQL com credenciais em `.env`
- PostgreSQL não incluído no repositório

## Configuração

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Para criar uma conta administrativa:

```powershell
python manage.py createsuperuser
```

O projeto usa um modelo de usuário personalizado (`users.User`). Ele precisa estar
configurado antes das primeiras migrações de autenticação. Bancos criados antes
desta alteração, com as migrações padrão de `auth` e `admin` aplicadas, não podem
ser reutilizados diretamente. Faça backup dos dados e configure um banco novo
antes de executar `python manage.py migrate`. Para desenvolvimento local com
SQLite, configure no `.env` um arquivo novo, por exemplo:

```env
DB_ENGINE=sqlite3
DB_NAME=biblioteca-auth.sqlite3
```

Livros anteriores à autenticação não têm responsável atribuído e ficam somente
para leitura; os novos cadastros registram automaticamente o usuário autenticado.
