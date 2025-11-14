# 📚 Sistema de Gerenciamento de Biblioteca – Python

Um sistema modular para gerenciamento de livros, autores, usuários e empréstimos, desenvolvido com foco em boas práticas, validações e testes automatizados.

---

## 🚀 Funcionalidades
- Cadastro de livros
- Cadastro de autores
- Cadastro de usuários
- Empréstimo e devolução
- Validações internas
- Usuários bloqueados
- Persistência JSON
- Testes unitários, integração e funcionais

---

## 🧱 Arquitetura

    /src

        /models
    
        /repositories
    
        /services
    
        /controllers
    
        /data
    
        /dao
    
        /exceptions
    
        /logs
    
        /ui
    
        /validators

    /tests
    
        /fixtures
        
        /mutation
        
        /specific
        
        /structural
        
        /unit
        
        /integration
        
        /functional
        
    /logs
    
    /htmlcov
    
    /docs
    
        projeto.md
        
        plano_testes.md
        
        relatorio.md

## 🧪 Testes
Para rodar:
(venv) PS E:\projetost\src> pytest -v ../tests/unit/test_unit_geral.py


## 📦 Instalação


git clone https://github.com/GuiJustica/projetost
pip install -r requirements.txt

python main.py ou python main_ui.py

