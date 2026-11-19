# Migração Django/SQLite para PostgreSQL

## Pesquisa

### SQLite x PostgreSQL
SQLite é um banco embutido em um arquivo, com configuração mínima. É adequado para estudos, protótipos, aplicativos desktop ou sites pequenos. PostgreSQL é um servidor completo, apropriado para concorrência, grandes volumes, integrações, recursos SQL avançados e aplicações reais.

### Driver
O Django usa o backend `django.db.backends.postgresql` e requer `psycopg` 3.1.8+ ou `psycopg2` 2.8.4+. Neste projeto usamos `psycopg[binary]`: `pip install "psycopg[binary]>=3.1.8"`.

### DATABASES
- ENGINE: backend usado pelo Django.
- NAME: nome da base PostgreSQL.
- USER: usuário que abre a conexão.
- PASSWORD: senha desse usuário.
- HOST: endereço do servidor; 127.0.0.1 usa TCP.
- PORT: porta do servidor; o padrão PostgreSQL é 5432.

### Criação segura do banco
Com um administrador autorizado, mas nunca usando o role postgres pela aplicação:

```sql
CREATE ROLE biblioteca_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD 'senha-forte';
CREATE DATABASE biblioteca OWNER biblioteca_app;
```

### Variáveis de ambiente
Variáveis de ambiente são pares nome/valor fornecidos ao processo pelo sistema ou por arquivos locais. Senhas não devem ficar no código nem no repositório. O código continua público, mas o `.env` real fica fora do Git.

### python-decouple
No `settings.py`, `config('DB_NAME')` lê o arquivo `.env` ou o ambiente do processo. `config(..., cast=bool/int/Csv())` converte os tipos.

### .gitignore e .env.example
`.gitignore` impede o envio do `.env` e do `db.sqlite3`. `.env.example` mostra os nomes das variáveis e valores fictícios, permitindo que outra pessoa configure o projeto.

### Outros segredos
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, credenciais de email, APIs e chaves criptográficas também devem sair do código e ser configuradas por ambiente.

## Implementação
- PostgreSQL com backend do Django.
- Credenciais carregadas por python-decouple.
- CRUD em `/`.
- Migração e carga via `dumpdata/loaddata`.

## Comandos
```powershell
python manage.py makemigrations livros
python manage.py migrate
python manage.py dumpdata --database=default --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission -o dados_sqlite.json
python manage.py loaddata dados_sqlite.json
python manage.py runserver
```

## Validação
Inclua nesta entrega os prints da criação do usuário/banco, `migrate`, listagem, cadastro, edição e exclusão.

## Fontes
- Django settings/DATABASES: https://docs.djangoproject.com/en/5.2/ref/settings/#databases
- Django PostgreSQL: https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes
- Django dumpdata/loaddata: https://docs.djangoproject.com/en/5.2/ref/django-admin/
- PostgreSQL CREATE DATABASE: https://www.postgresql.org/docs/current/sql-createdatabase.html
- PostgreSQL CREATE ROLE: https://www.postgresql.org/docs/current/sql-createrole.html
- python-decouple: https://github.com/HBNetwork/python-decouple

## Trechos do settings.py

### Antes

```python
SECRET_KEY = 'django-insecure-valor-gerado-pelo-django'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Depois

```python
from decouple import Csv, config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}
```

## Migração dos dados SQLite

No banco SQLite original:

```powershell
python manage.py dumpdata livros --natural-foreign --natural-primary --output dados_sqlite.json
```

Depois de criar o banco PostgreSQL e executar `python manage.py migrate`:

```powershell
python manage.py loaddata dados_sqlite.json
python manage.py shell -c "from django.db import connection; print(connection.vendor)"
python manage.py sqlsequencereset livros
```

Os dados são carregados por `loaddata` somente depois das tabelas terem sido criadas no PostgreSQL.
