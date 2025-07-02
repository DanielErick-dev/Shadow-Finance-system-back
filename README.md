# Shadow Finance System - Back-End

API RESTful robusta e segura, construída com Python, Django e Django REST Framework para servir como a espinha dorsal do sistema Shadow Finance.

## 🚀 Sobre o Projeto

Este repositório contém o código do **Back-End** do sistema Shadow Finance. Ele é responsável por toda a lógica de negócio, segurança, manipulação de dados e por fornecer os endpoints que o frontend consome.

A arquitetura foi projetada para ser segura e escalável, com um sistema de autenticação baseado em JWT (JSON Web Tokens) e regras de permissão que garantem que cada usuário só possa acessar e manipular seus próprios dados.

**🔗 Link para o repositório do Front-End:** https://github.com/DanielErick-dev/Shadow-Finance-system-front

---

## 🌟 Principais Funcionalidades da API

- **🔐 Autenticação com JWT:** Sistema de autenticação completo com tokens de acesso e de atualização (`refresh tokens`) usando a biblioteca `djangorestframework-simplejwt`.
- **🛡️ Endpoints Seguros:** Cada endpoint é protegido, garantindo que apenas usuários autenticados possam realizar operações. A lógica de negócio assegura o isolamento total dos dados entre os usuários.
- **📈 CRUD Completo:** Endpoints RESTful completos para todas as entidades principais do sistema:
    - Gestão de Ativos (`/api/v1/ativos/`)
    - Gestão de Cards de Mês de Dividendos (`/api/v1/cards-dividendos/`)
    - Gestão de Itens de Dividendo individuais (`/api/v1/itens-dividendos/`)
- **⚙️ Paginação e Filtragem:** Suporte nativo para paginação e filtragem nos endpoints de listagem, garantindo alta performance mesmo com grandes volumes de dados.
- **✅ Validação de Dados:** Regras de validação robustas no nível do modelo e do serializer para garantir a integridade e a consistência dos dados.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
|---|---|
| **Python** | Linguagem de programação principal. |
| **Django** | Framework web robusto para a estrutura do projeto. |
| **Django REST Framework (DRF)** | Toolkit poderoso para construir APIs Web. |
| **Simple JWT** | Para implementação da autenticação baseada em JSON Web Tokens. |
| **django-filter** | Para adicionar suporte a filtragem avançada nos endpoints. |
| **django-cors-headers** | Para gerenciar as permissões de Cross-Origin Resource Sharing (CORS). |
| **SQLite** | Banco de dados padrão para o ambiente de desenvolvimento. |

---

## ⚙️ Como Rodar o Projeto (Back-End)

**Pré-requisitos:**
- Python 3.x instalado.
- Um gerenciador de pacotes como `pip`.

**Passos:**
1.  Clone o repositório:
    ```bash
    git clone https://github.com/DanielErick-dev/Shadow-Finance-system-back.git
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd Shadow-Finance-System-back
    ```
3.  Crie e ative um ambiente virtual:
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
5.  Crie um arquivo `.env` na raiz do projeto, baseado no arquivo `.env.example` e configure suas variáveis de ambiente

6.  Aplique as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```
7.  Crie um superusuário para acessar a área administrativa:
    ```bash
    python manage.py createsuperuser
    ```
8.  Execute o servidor de desenvolvimento:
    ```bash
    # Para acesso local e de outros dispositivos na mesma rede
    python manage.py runserver 0.0.0.0:8000
    ```
9.  A API estará disponível em `http://127.0.0.1:8000/api/v1/`.

---

## 📝 Roadmap e Próximos Passos

- [ ] Implementação dos endpoints para o módulo de **Controle de Despesas**.
- [ ] Criação dos modelos e endpoints para a **Evolução de Investimentos**.
- [ ] Desenvolvimento de endpoints de agregação para o **Dashboard**.
- [ ] Refatorar a autenticação para usar **Cookies HttpOnly** para o refresh token em produção.
- [ ] substituir sqlite por banco de dados postgres
