# Sistema de Gerenciamento de Biblioteca – Documentação do Projeto

## 1. Introdução
Este projeto implementa um sistema modular para gerenciamento de bibliotecas, incluindo cadastro de livros, autores, usuários e controle de empréstimos. A aplicação foi projetada com foco em estrutura limpa, validação robusta, testes unitários e testes de integração completos, simulando cenários reais de uso.

## 2. Arquitetura do Sistema
A aplicação segue uma arquitetura dividida em módulos:

### 2.1 Models
Representam as entidades principais do domínio:
- `Livro`
- `Autor`
- `Usuario`
- `Emprestimo`

### 2.2 Repositórios
Camada responsável pelo armazenamento e manipulação dos dados:
- `LivroRepository`
- `AutorRepository`
- `UsuarioRepository`
- `EmprestimoRepository`

### 2.3 Services
Camada que implementa regras de negócio:
- `ArquivoService`
- `EmprestimoService`
- `UsuarioService` (opcional)

### 2.4 Controllers
Responsável por orquestrar todos os módulos:
- `BibliotecaController`

## 3. Funcionalidades Principais
- Cadastro, edição e exclusão de livros
- Cadastro e manutenção de autores
- Registro de usuários
- Empréstimo e devolução de livros
- Bloqueio de usuários inadimplentes
- Persistência em JSON
- Listagem e busca
- Regras de validação fortes

## 4. Regras de Negócio
- Livros não podem ser emprestados se estiverem indisponíveis.
- Usuários bloqueados não podem realizar empréstimos.
- Um empréstimo deve ter livro, usuário e datas válidas.
- Títulos de livros e nomes de autores devem ser válidos.
- Persistência deve refletir exatamente o estado atual do sistema.

## 5. Estrutura de Pastas

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

README.md


## 6. Tecnologias Utilizadas
- Python 3.x
- Pytest
- JSON
- Arquitetura orientada a objetos
