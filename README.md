# Inventory Control API

Sistema de controle de estoque, validade e reposicao para pequenos comercios.

## Descricao

O projeto tem como objetivo construir uma aplicacao web baseada em microsservicos para apoiar pequenos mercados, mercearias, restaurantes e lanchonetes no controle de produtos, estoque, validade e reposicao.

## Problema escolhido

Pequenos comercios perdem dinheiro por falta de controle sobre entradas e saidas de produtos, acompanhamento manual de estoque minimo e baixa visibilidade sobre itens proximos do vencimento.

## Solucao proposta

A solucao proposta e uma aplicacao web composta por microsservicos para cadastro de produtos, controle de itens em estoque, registro de movimentacoes, alertas de estoque baixo e alertas de vencimento proximo.

## Stack planejada

- Python
- FastAPI
- Pydantic
- Pytest
- Behave ou pytest-bdd
- Docker
- HTML, CSS e JavaScript puro

## Microsservicos planejados

- product-service: responsavel pelo cadastro e consulta de produtos.
- inventory-service: responsavel pelo controle de estoque, movimentacoes, estoque minimo e alertas.

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

## Execucao final planejada

Ao final do projeto, a aplicacao sera executada com Docker Compose, subindo os microsservicos FastAPI e o frontend em portas separadas:

- product-service: `8081`
- inventory-service: `8082`
- frontend: `3000`
