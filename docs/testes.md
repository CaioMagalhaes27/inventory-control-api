# Testes

Cada microsservico tem sua propria suite de testes baseada em **pytest** + FastAPI **TestClient**.
Os testes exercitam a API ponta a ponta, atravessando router -> use case -> factory -> repository,
o que valida tanto as regras de dominio quanto a serializacao Pydantic e os exception handlers.

## Como rodar

```bash
cd services/product-service && pytest -v
cd services/inventory-service && pytest -v
```

## Resultado atual

| Servico            | Testes | Status |
|--------------------|--------|--------|
| product-service    | 12     | passing |
| inventory-service  | 15     | passing |
| **Total**          | **27** | **passing** |

## product-service - cenarios cobertos

`services/product-service/tests/test_products.py`

1. Criar produto valido.
2. `name` obrigatorio.
3. `sku` obrigatorio.
4. `sku` duplicado (`DUPLICATE_SKU`).
5. `minimumStock` negativo.
6. Listar produtos.
7. Buscar por id.
8. Buscar inexistente (`PRODUCT_NOT_FOUND`).
9. Atualizar produto.
10. Atualizar inexistente.
11. Soft delete.
12. Deletar inexistente.

## inventory-service - cenarios cobertos

`services/inventory-service/tests/test_stock.py`

1. Criar item valido.
2. `productId` obrigatorio.
3. `quantity` negativa.
4. `minimumStock` negativo.
5. Listar itens.
6. Buscar por id.
7. Buscar inexistente (`STOCK_ITEM_NOT_FOUND`).
8. Entrada valida (quantidade aumenta).
9. Entrada invalida (quantity = 0).
10. Saida valida (quantidade diminui).
11. Saida invalida (quantity = 0).
12. Estoque insuficiente (`INSUFFICIENT_STOCK`).
13. Listar estoque baixo (`/low-stock`).
14. Listar proximos do vencimento (`/expiring`).
15. Recusar `expirationDate` no passado.

## Estrategia

- Testes de API com `TestClient` (httpx). Sem mocks de banco - o `InMemoryProductRepository` e `InMemoryStockItemRepository` ja sao implementacoes de producao das interfaces de dominio, entao os testes refletem comportamento real.
- Cada teste recebe um `client` novo via fixture, com repositorios zerados em cada execucao, garantindo isolamento.
- Regras de negocio (SKU duplicado, estoque insuficiente, validade futura, baixa de estoque) sao validadas por `assert` no codigo de status HTTP e no campo `code` do payload de erro.
- Codigos de erro padronizados (`PRODUCT_NOT_FOUND`, `DUPLICATE_SKU`, `STOCK_ITEM_NOT_FOUND`, `INSUFFICIENT_STOCK`, `VALIDATION_ERROR`) facilitam consumo pelo frontend.

## TDD

A cobertura acima foi escrita junto com a implementacao, exercitando o ciclo red -> green -> refactor para cada caso de uso (`CreateProduct`, `RegisterMovement`, etc.). As factories concentram a validacao para que os mesmos testes cubram tambem o fluxo de criacao direta de entidades.
