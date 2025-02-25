Documentação do Projeto Django: CRUD de CEPs
Visão Geral
Este projeto é uma aplicação Django que permite criar, listar, atualizar e deletar registros de CEPs. Ele utiliza a API do ViaCEP para buscar informações de endereço a partir de um CEP fornecido pelo usuário.

Estrutura do Projeto
Diretórios e Arquivos Principais
Copy
projeto_django/
│
├── crud/                        # App principal do projeto
│   ├── migrations/              # Migrações do banco de dados
│   ├── templates/               # Templates HTML
│   │   └── crud/                # Subpasta para templates da app
│   │       ├── form_cep.html    # Template para criar/editar CEPs
│   │       ├── lista_cep.html   # Template para listar CEPs
│   │       └── deleta_cep.html  # Template para deletar CEPs
│   ├── __init__.py
│   ├── admin.py                 # Configuração do admin do Django
│   ├── apps.py                  # Configuração da app
│   ├── forms.py                 # Formulários da app
│   ├── models.py                # Modelos de dados
│   ├── tests.py                 # Testes da app
│   ├── urls.py                  # URLs da app
│   └── views.py                 # Views da app
│
├── projeto/                     # Configurações do projeto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # Configurações do projeto
│   ├── urls.py                  # URLs globais do projeto
│   └── wsgi.py
│
├── db.sqlite3                   # Banco de dados SQLite
├── manage.py                    # Script de gerenciamento do Django
└── requirements.txt             # Dependências do projeto
Funcionalidades
1. Criação de CEP
O usuário pode inserir um CEP no formulário.

O sistema consulta a API do ViaCEP para obter os dados do endereço.

Se o CEP for válido, os dados são salvos no banco de dados.

2. Listagem de CEPs
Exibe todos os CEPs cadastrados em uma tabela.

Permite visualizar os detalhes de cada CEP.

3. Atualização de CEP
Permite editar os dados de um CEP existente.

Atualiza os dados no banco de dados.

4. Exclusão de CEP
Permite deletar um CEP do banco de dados.

Modelos de Dados
CepModel
Este modelo representa um registro de CEP no banco de dados.

python
Copy
from django.db import models

class CepModel(models.Model):
    cep = models.CharField(max_length=9, unique=True)  # CEP (formato: 00000-000)
    cidade = models.CharField(max_length=100)          # Cidade

    def __str__(self):
        return self.cep
Views
1. CepCreateView
Responsabilidade: Cria um novo registro de CEP.

Método HTTP: GET (exibe o formulário) e POST (processa o formulário).

Template: crud/form_cep.html

python
Copy
import requests
from django.views.generic import FormView
from django.urls import reverse_lazy
from .models import CepModel
from .forms import cepForm

class CepCreateView(FormView):
    template_name = 'crud/form_cep.html'
    form_class = cepForm
    success_url = reverse_lazy('lista_cep')

    def form_valid(self, form):
        cep = form.cleaned_data['cep']
        url = f'https://viacep.com.br/ws/{cep}/json/'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados_endereco = resposta.json()
            CepModel.objects.create(
                cep=cep,
                cidade=dados_endereco.get('localidade')
            )
        return super().form_valid(form)
2. CepListView
Responsabilidade: Lista todos os CEPs cadastrados.

Método HTTP: GET.

Template: crud/lista_cep.html

python
Copy
from django.views.generic import ListView
from .models import CepModel

class CepListView(ListView):
    model = CepModel
    template_name = 'crud/lista_cep.html'
3. CepUpdateView
Responsabilidade: Atualiza um registro de CEP existente.

Método HTTP: GET (exibe o formulário) e POST (processa o formulário).

Template: crud/form_cep.html

python
Copy
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import CepModel

class CepUpdateView(UpdateView):
    model = CepModel
    fields = ['cep', 'cidade']
    template_name = 'crud/form_cep.html'
    success_url = reverse_lazy('lista_cep')
4. CepDeleteView
Responsabilidade: Deleta um registro de CEP.

Método HTTP: GET (exibe confirmação) e POST (processa a exclusão).

Template: crud/deleta_cep.html

python
Copy
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import CepModel

class CepDeleteView(DeleteView):
    model = CepModel
    template_name = 'crud/deleta_cep.html'
    success_url = reverse_lazy('lista_cep')
URLs
URLs Globais (projeto/urls.py)
Define as URLs globais do projeto.

python
Copy
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('crud.urls')),  # Inclui as URLs da app crud
]
URLs da App (crud/urls.py)
Define as URLs da app crud.

python
Copy
from django.urls import path
from .views import CepCreateView, CepListView, CepUpdateView, CepDeleteView

urlpatterns = [
    path('criar/', CepCreateView.as_view(), name='criar_cep'),
    path('lista/', CepListView.as_view(), name='lista_cep'),
    path('editar/<int:pk>/', CepUpdateView.as_view(), name='editar_cep'),
    path('deletar/<int:pk>/', CepDeleteView.as_view(), name='deletar_cep'),
]
Templates
1. form_cep.html
Formulário para criar ou editar um CEP.

html
Copy
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário de CEP</title>
</head>
<body>
    <h1>Formulário de CEP</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
    </form>
</body>
</html>
Run HTML
2. lista_cep.html
Lista todos os CEPs cadastrados.

html
Copy
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de CEPs</title>
</head>
<body>
    <h1>Lista de CEPs</h1>
    <ul>
        {% for cep in object_list %}
            <li>{{ cep.cep }} - {{ cep.cidade }}</li>
        {% endfor %}
    </ul>
</body>
</html>
Run HTML
3. deleta_cep.html
Confirmação para deletar um CEP.

html
Copy
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deletar CEP</title>
</head>
<body>
    <h1>Deletar CEP</h1>
    <p>Tem certeza que deseja deletar o CEP "{{ object.cep }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Confirmar</button>
    </form>
</body>
</html>
Run HTML
Como Executar o Projeto
1. Instale as Dependências
Certifique-se de ter o Python instalado. Em seguida, instale as dependências do projeto:

bash
Copy
pip install -r requirements.txt
2. Execute as Migrações
Crie e aplique as migrações do banco de dados:

bash
Copy
python manage.py makemigrations
python manage.py migrate
3. Inicie o Servidor
Execute o servidor de desenvolvimento:

bash
Copy
python manage.py runserver
4. Acesse o Projeto
Abra o navegador e acesse:

Criar CEP: http://127.0.0.1:8000/api/criar/

Listar CEPs: http://127.0.0.1:8000/api/lista/

Conclusão
Este projeto é um exemplo básico de CRUD (Create, Read, Update, Delete) usando Django. Ele pode ser expandido com mais funcionalidades, como autenticação de usuários, validações adicionais e integração com outras APIs.