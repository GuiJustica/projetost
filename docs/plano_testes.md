# Plano de Testes – Sistema de Biblioteca

## 1. Objetivo
Garantir a qualidade do sistema através de testes unitários, de integração e funcionais, cobrindo todas as funcionalidades críticas do projeto.

---

## 2. Tipos de Testes

### 2.1 Testes Unitários
Objetivo: validar componentes isolados.

Abrangem:
- Validações dos models
- Regras de negócio
- Repositórios
- Services

Ferramentas:
- Pytest
- Parametrização
- Fixtures

Exemplos testados:
- Validação de títulos
- Ano inválido
- Nome de autor vazio
- Empréstimo de livro indisponível

---

### 2.2 Testes de Integração
Objetivo: validar interações entre módulos.

Fluxos testados:
- Criar autor → livro → usuário → empréstimo
- Persistência JSON
- Fluxo completo: cadastro, empréstimo e devolução
- Rollback em caso de falha
- Usuário bloqueado
- Livro indisponível

Requisito mínimo: **10 testes integrados**
Status: **Atendido**

---

### 2.3 Testes Funcionais
Simulam a utilização real do sistema.

Cenários testados:
- Fluxo completo de empréstimo
- Devolução
- Listagem de disponíveis
- Interação total com o controller

---

## 3. Critérios de Aceitação
- Todos os testes devem passar
- Exceções corretas devem ser levantadas
- Persistência deve ser fiel
- Regras de negócio devem ser respeitadas

---

## 4. Métricas e Cobertura
Resultados finais obtidos:

- **Total de testes:** *exemplo: 48*
- **Unitários:** 32
- **Integração:** 10
- **Funcionais:** 6

Execução final:

