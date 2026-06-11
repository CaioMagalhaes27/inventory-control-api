# Entrega

## Problema escolhido

Sistema de controle de estoque, validade e reposicao para pequenos comercios.

Pequenos mercados, mercearias, restaurantes e lanchonetes podem perder dinheiro por falta de controle sobre quantidade em estoque, produtos proximos do vencimento, estoque minimo e registros manuais de entrada e saida.

## Publico-alvo

O publico-alvo sao pequenos comercios que precisam organizar produtos, lotes, validade e reposicao sem depender de sistemas caros ou complexos.

## Solucao proposta

A solucao e uma aplicacao web com dois microsservicos:

- `product-service`: responsavel pelo cadastro e gerenciamento de produtos.
- `inventory-service`: responsavel por itens de estoque, movimentacoes, estoque baixo e alertas de validade.

O frontend em HTML/CSS/JS puro permite operar o sistema pelo navegador, consumindo as APIs dos microsservicos.

## Funcionalidades principais

- Cadastro, listagem, atualizacao e soft delete de produtos.
- Cadastro e listagem de itens de estoque.
- Registro de entrada de estoque.
- Registro de saida de estoque.
- Alertas de estoque baixo.
- Alertas de produtos proximos do vencimento.
- Dashboard com indicadores operacionais.
- Persistencia local com SQLite por microsservico.

## Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- Behave/Gherkin
- Docker
- HTML/CSS/JS puro

## Conceitos academicos demonstrados

- Clean Code
- SOLID
- Design Patterns
- TDD
- BDD
- Arquitetura Limpa
- Microsservicos
- Docker
- Deploy

## Justificativa tecnica

Python com FastAPI permite criar APIs simples, testaveis e bem documentadas. A separacao em microsservicos divide responsabilidades entre produtos e estoque. A Arquitetura Limpa isola regras de negocio de detalhes de banco, HTTP e infraestrutura. SQLAlchemy com SQLite fornece persistencia local por servico, mantendo independencia entre os bancos.
