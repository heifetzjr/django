#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

"""
1 - Estrutura de um projeto Django
manage.py          # Ferramenta de linha de comando do projeto
projeto/
    __init__.py
    settings.py    # Configurações gerais (banco, apps, timezone...)
    urls.py        # Rotas principais do projeto
    wsgi.py        # Servidor web (produção)
    asgi.py        # Servidor assíncrono

2 - CICLO DE UMA REQUISIÇÃO:
Usuário acessa URL
      ↓
urls.py (roteia para a view correta)
      ↓
views.py (processa a lógica, busca dados)
      ↓
models.py (acessa o banco de dados)
      ↓
template HTML (renderiza a resposta)
      ↓
Usuário vê a página

3 - RODAR SERVIDOR
python manage.py runserver

4 - CRIAR APP
python manage.py startapp school

5 - Agora, registrar o app nas configurações do projeto:

No arquivo core/settings.py, em INSTALLED_APPS, adicione 'school',:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'school',  # nosso app
]

6 - Primeiro Model (M do MVT)

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
        
Alguns pontos importantes:

CharField → textos curtos (obrigatório max_length)
EmailField → já faz validação básica de e-mail
DateField → datas
auto_now_add=True → define automaticamente na criação

7 - Criar a tabela no banco (migrations)
python manage.py makemigrations school
python manage.py migrate

makemigrations → Django lê os models e cria arquivos de migração.
migrate → aplica essas migrações ao banco (por padrão, db.sqlite3).

8 - Registrar no Admin  
No school/admin.py:

from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'birth_date', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('birth_date', 'created_at')
    
Criar um superusuário:
python manage.py createsuperuser

rode o servidor

9 - Views + URLs + Templates (V e T do MVT)
Agora vamos exibir a lista de estudantes em uma página pública.
No school/views.py:

from django.shortcuts import render
from .models import Student

def student_list(request):
    students = Student.objects.all().order_by('name')
    context = {
        'students': students,
    }
    return render(request, 'school/student_list.html', context)
    
10 - URLs do app
Crie o arquivo school/urls.py (pode não existir ainda):

from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
]

11 - Conectar URLs do app nas URLs do projeto
No core/urls.py, importe include e conecte as rotas:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),  # rota raiz envia para o app school
]

Agora, ao acessar http://127.0.0.1:8000/students/, a view student_list será chamada.

12 - Templates
Vamos criar uma estrutura de templates organizada.

Na raiz do projeto (onde está manage.py), crie uma pasta templates/, e dentro dela uma pasta school/:

templates/
└─ school/
   └─ student_list.html
   
No core/settings.py, adicione o caminho da pasta templates na configuração TEMPLATES:

from pathlib import Path
import os  # se ainda não tiver

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],  # adiciona essa linha
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

Agora, no templates/school/student_list.html:

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Estudantes</title>
</head>
<body>
    <h1>Lista de Estudantes</h1>

    {% if students %}
        <ul>
            {% for student in students %}
                <li>
                    {{ student.name }} - {{ student.email }}
                    {% if student.birth_date %}
                        ({{ student.birth_date }})
                    {% endif %}
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Nenhum estudante cadastrado.</p>
    {% endif %}
</body>
</html>

Se você já cadastrou estudantes no admin, eles devem aparecer nessa página.


"""