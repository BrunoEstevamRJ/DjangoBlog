📝 Django Blog

Um blog simples criado com Django, onde usuários podem criar, editar e visualizar postagens.
🚀 Funcionalidades

    📌 Cadastro e login de usuários
    ✍️ Criação e edição de postagens
    📄 Listagem de posts com ordenação do mais recente para o mais antigo
    🔒 Controle de acesso: apenas o autor pode editar seus posts
    🎨 Interface responsiva com Bootstrap

🛠 Tecnologias utilizadas

    Django - Framework principal
    Bootstrap - Estilização
    SQLite (ou outro banco de dados configurável)
    HTML/CSS/JavaScript - Para renderização das páginas

📌 Pré-requisitos

Antes de começar, você precisará ter instalado:

    Python 3.8+
    pip e venv (ambiente virtual recomendado)

📦 Instalação

    Clone o repositório:

git clone https://github.com/seu-usuario/django-blog.git
cd django-blog

Crie um ambiente virtual e ative:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

Instale as dependências:

pip install -r requirements.txt

Execute as migrações para configurar o banco de dados:

python manage.py migrate

Crie um superusuário (opcional, para acessar o admin do Django):

python manage.py createsuperuser

Inicie o servidor local:

    python manage.py runserver

    Acesse o blog em http://127.0.0.1:8000/ 🚀

🏗 Estrutura do projeto

django-blog/
│── blog/                  # App principal
│   ├── templates/         # Arquivos HTML
│   ├── static/            # CSS, JS, Imagens
│   ├── models.py          # Modelo de Post
│   ├── views.py           # Lógica das páginas
│   ├── urls.py            # Rotas do blog
│   ├── forms.py           # Formulários de postagens
│── mysite/                # Configuração do projeto
│   ├── settings.py        # Configurações do Django
│   ├── urls.py            # Rotas principais
│── db.sqlite3             # Banco de dados SQLite (padrão)
│── manage.py              # Gerenciador do Django
│── requirements.txt       # Dependências do projeto

📌 Melhorias futuras

    🗃 Adição de categorias e tags para organização das postagens
    💬 Comentários em posts para interação entre usuários
    📅 Agendamento de postagens para publicação futura

🤝 Contribuindo

Se quiser contribuir:

    Faça um fork do repositório
    Crie uma branch para sua feature (git checkout -b DjangoBlog)
    Faça o commit (git commit -m 'Adiciona nova funcionalidade')
    Suba as mudanças (git push origin DjangoBlog)
    Abra um Pull Request 🎉

📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
