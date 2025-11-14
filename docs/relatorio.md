# Relatório Final – Sistema de Gerenciamento de Biblioteca

## 1. Introdução
Este relatório apresenta o desenvolvimento de um sistema de gerenciamento de biblioteca construído em Python. O projeto foi estruturado com foco em arquitetura modular, testes automatizados e qualidade do código, simulando um sistema real utilizado em ambientes profissionais.

---

## 2. Desenvolvimento

### 2.1 Implementação das Entidades
Foram implementados models robustos com validações internas e regras de integridade, impedindo objetos inconsistentes.

### 2.2 Regras de Negócio
O controle de empréstimos foi projetado para:
- Impedir empréstimo de livros indisponíveis
- Impedir ações de usuários bloqueados
- Garantir integridade nas relações livro–usuário

### 2.3 Persistência
O sistema conta com persistência em JSON por meio do `ArquivoService`, permitindo salvar e recuperar livros com segurança e consistência.

---

## 3. Testes Automatizados

### 3.1 Testes Unitários
Validam:
- Models
- Services
- Validações
- Repositórios

### 3.2 Testes de Integração
Validam:
- Fluxo completo de empréstimo
- Persistência em JSON
- Múltiplas interações entre módulos
- Regras combinadas de disponibilidade e bloqueio

---

## 4. Resultados
- Todos os testes passaram com sucesso
- A arquitetura ficou consistente e expansível
- O sistema está pronto para evoluções futuras (API REST, banco SQL, UI)

---

## 5. Conclusão
O projeto demonstrou a importância de boas práticas de engenharia de software, como modularização, testes automatizados e validação rigorosa. A aplicação está confiável, extensível e adequada como base para sistemas maiores, além de servir como um estudo sólido de qualidade de software.

