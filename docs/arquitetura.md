# Arquitetura

Dois microsservicos independentes em Python/FastAPI, ambos seguindo Arquitetura Limpa em quatro camadas.

## Visao geral

```
+---------------------+        +-----------------------+
|   product-service   |        |   inventory-service   |
|   :8081             |        |   :8082               |
+---------------------+        +-----------------------+
        |                              |
        |  produtos (CRUD + SKU)       |  estoque + movimentos
```

Os servicos nao compartilham banco. A integracao entre `productId` no inventory e o produto em si e feita por referencia (string), permitindo evolucao independente.

## Stack

- FastAPI (HTTP + OpenAPI automatica)
- Pydantic v2 (schemas e validacao de payload)
- Uvicorn (ASGI)
- Pytest + httpx (testes de integracao via `TestClient`)

## Camadas

Cada servico segue o mesmo layout:

```
app/
├── main.py                       # FastAPI factory + bootstrap
├── domain/                       # regras de negocio puras
│   ├── entities/                 # Product, StockItem, StockMovement, MovementType
│   ├── repositories/             # interfaces abstratas (Repository pattern)
│   └── exceptions/               # erros de dominio
├── application/                  # casos de uso e orquestracao
│   ├── use_cases/                # CreateProduct, RegisterMovement, ...
│   ├── schemas/                  # Pydantic request/response (DTOs)
│   ├── factories/                # construcao validada de entidades
│   └── mappers/                  # entidade <-> response
├── infrastructure/
│   └── repositories/             # implementacao in-memory
└── presentation/
    ├── routers/                  # rotas FastAPI
    └── exception_handlers/       # traducao de erros -> HTTP
```

### Regras de dependencia

- `presentation` depende de `application`
- `application` depende de `domain`
- `infrastructure` implementa interfaces de `domain`
- `domain` nao depende de ninguem

Isso mantem regras de negocio isoladas de FastAPI e de detalhes de persistencia.

## Patterns aplicados

| Pattern    | Onde                                                     | Por que                                                     |
|------------|----------------------------------------------------------|-------------------------------------------------------------|
| Repository | `domain/repositories` + `infrastructure/repositories`    | Isola persistencia. Permite trocar in-memory por DB depois. |
| Factory    | `application/factories`                                  | Centraliza validacao na construcao das entidades.           |
| Mapper     | `application/mappers`                                    | Converte entidade <-> response sem vazar camadas.           |
| Strategy   | `application/use_cases/movement_strategy.py` (inventory) | `EntryStrategy` e `ExitStrategy` aplicam regras distintas.  |

## product-service

Entidade `Product` com campos:
`id, name, description, sku, category, unit, minimumStock, active, createdAt, updatedAt`.

Rotas:
- `POST /api/products`
- `GET /api/products`
- `GET /api/products/{id}`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}` (soft delete via `active = false`)

Regras: `name`, `sku` e `unit` obrigatorios; `sku` unico entre produtos ativos; `minimumStock >= 0`.

Erros de dominio: `PRODUCT_NOT_FOUND` (404), `DUPLICATE_SKU` (409), `VALIDATION_ERROR` (422).

## inventory-service

Entidades:
- `StockItem`: `id, productId, quantity, minimumStock, expirationDate, batchCode, active, createdAt, updatedAt`
- `StockMovement`: `id, stockItemId, productId, type, quantity, reason, occurredAt`
- `MovementType`: enum `ENTRY` / `EXIT`

Rotas:
- `POST /api/stock-items`
- `GET /api/stock-items`
- `GET /api/stock-items/{id}`
- `POST /api/stock-items/{id}/entries`
- `POST /api/stock-items/{id}/exits`
- `GET /api/stock-items/low-stock`
- `GET /api/stock-items/expiring`

Regras:
- `productId` obrigatorio
- `quantity >= 0` no cadastro
- `minimumStock >= 0`
- entrada > 0, saida > 0
- saida nao pode deixar `quantity < 0`
- `expirationDate`, quando informada, precisa ser futura
- estoque baixo quando `quantity <= minimumStock`
- vencimento proximo: 30 dias

Erros de dominio: `STOCK_ITEM_NOT_FOUND` (404), `INSUFFICIENT_STOCK` (409), `VALIDATION_ERROR` (422).

## Tratamento de erros

`presentation/exception_handlers/handlers.py` registra dois handlers:
- erros de dominio (`DomainError`) -> JSON `{ code, message }` com status mapeado;
- `RequestValidationError` do FastAPI -> `VALIDATION_ERROR` 422 com `details`.

## Persistencia

Implementacao atual e in-memory (dicionarios). Como o acesso e feito via interface (`ProductRepository`, `StockItemRepository`, `StockMovementRepository`), uma futura implementacao com banco e plugavel sem alterar `application` ou `presentation`.

## Principios SOLID

- SRP: cada classe (factory, mapper, use case, strategy) tem uma responsabilidade.
- OCP: novos tipos de movimento sao adicionados criando novas `MovementStrategy` sem alterar use cases.
- LSP: `InMemoryProductRepository` substitui `ProductRepository` sem quebrar consumidores.
- ISP: interfaces de repositorio contem apenas os metodos usados.
- DIP: use cases recebem repositorios via construtor (injecao manual), dependendo de abstracoes.
