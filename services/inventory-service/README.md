# inventory-service

FastAPI service for stock items and movements (entries/exits).

## Stack
- FastAPI + Pydantic
- Uvicorn
- Pytest

## Run
```bash
cd services/inventory-service
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
uvicorn app.main:app --port 8082 --reload
```

## Tests

Unit + API tests:
```bash
pytest
```

BDD scenarios (behave + Gherkin):
```bash
behave
```

The `features/` folder contains the `.feature` files and step definitions used by `behave`.

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/stock-items | Create stock item |
| GET | /api/stock-items | List stock items |
| GET | /api/stock-items/{id} | Get item |
| POST | /api/stock-items/{id}/entries | Register entry (ENTRY) |
| POST | /api/stock-items/{id}/exits | Register exit (EXIT) |
| GET | /api/stock-items/low-stock | Items with quantity <= minimumStock |
| GET | /api/stock-items/expiring | Items expiring within 30 days |

## Patterns
- Repository (domain interface + in-memory impl)
- Factory (StockItemFactory, MovementFactory)
- Strategy (EntryStrategy / ExitStrategy)
- Mapper (entity <-> response)

## Error codes
- `STOCK_ITEM_NOT_FOUND` (404)
- `INSUFFICIENT_STOCK` (409)
- `VALIDATION_ERROR` (422)
