# Arquitetura

## Visao geral

O projeto e uma aplicacao web para controle de estoque, validade e reposicao para pequenos comercios.

A solucao foi organizada em dois microsservicos independentes:

- `product-service`, exposto em `localhost:8081`.
- `inventory-service`, exposto em `localhost:8082`.

Cada servico possui sua propria API FastAPI, suas regras de negocio e seu proprio banco SQLite.

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

## Camadas da Arquitetura Limpa

Cada microsservico segue a divisao abaixo:

- `domain`: entidades de negocio, interfaces de repositorio e excecoes de dominio.
- `application`: casos de uso, schemas Pydantic, factories e mappers.
- `infrastructure`: configuracao de banco, modelos SQLAlchemy e repositorios concretos.
- `presentation`: rotas FastAPI, injecao dos repositorios e exception handlers.

Regras de dependencia:

- `presentation` chama `application`.
- `application` depende de abstracoes do `domain`.
- `infrastructure` implementa contratos definidos no `domain`.
- `domain` nao depende de FastAPI, SQLAlchemy ou Docker.

## Microsservicos

### product-service

Responsavel por produtos.

Campos persistidos:

- `id`
- `name`
- `description`
- `sku`
- `category`
- `unit`
- `minimumStock`
- `active`
- `createdAt`
- `updatedAt`

Principais rotas:

- `POST /api/products`
- `GET /api/products`
- `GET /api/products/{id}`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`

O delete de produto e soft delete, mantendo o registro persistido e alterando `active` para `false`.

### inventory-service

Responsavel por itens de estoque e movimentacoes.

Entidades principais:

- `StockItem`
- `StockMovement`
- `MovementType`

Principais rotas:

- `POST /api/stock-items`
- `GET /api/stock-items`
- `GET /api/stock-items/{id}`
- `POST /api/stock-items/{id}/entries`
- `POST /api/stock-items/{id}/exits`
- `GET /api/stock-items/low-stock`
- `GET /api/stock-items/expiring`

## Banco de dados

Cada microsservico possui seu proprio SQLite:

- `services/product-service/data/products.db`
- `services/inventory-service/data/inventory.db`

Os bancos sao independentes e nao sao versionados. Os arquivos `.db` ficam ignorados pelo Git para evitar versionar dados locais de execucao.

## Design Patterns usados

- Repository: contratos no `domain` e implementacoes em `infrastructure`.
- Factory: criacao validada de entidades.
- Mapper: conversao entre entidade de dominio e schemas de resposta.
- Strategy: regras diferentes para entrada e saida de estoque no inventory-service.

## Principios SOLID

- SRP: cada classe tem uma responsabilidade clara.
- OCP: regras podem ser estendidas sem alterar contratos centrais.
- LSP: repositorios in-memory e SQLAlchemy substituem as mesmas interfaces.
- ISP: interfaces de repositorio possuem apenas os metodos necessarios.
- DIP: casos de uso dependem de abstracoes, nao de implementacoes concretas.

## Conceitos obrigatorios

- Clean Code
- SOLID
- Design Patterns
- TDD
- BDD
- Arquitetura Limpa
- Microsservicos
- Docker
- Deploy
