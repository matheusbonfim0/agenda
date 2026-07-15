# Agenda

Aplicação Django para criar e gerenciar eventos privados por usuário.

## Executar localmente

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Copie `.env.example` para o gerenciador de variáveis do seu ambiente. Em produção,
defina uma chave secreta nova, mantenha `DJANGO_DEBUG=false` e configure os hosts permitidos.

## Testes

```bash
python manage.py test
python manage.py check --deploy
```
