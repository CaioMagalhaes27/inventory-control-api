# product-service

FastAPI service exposing CRUD for products.

## Stack
- FastAPI + Pydantic
- Uvicorn
- Pytest

## Run
```bash
cd services/product-service
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
uvicorn app.main:app --port 8081 --reload
```

## Tests
```bash
pytest
```

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/products | Create product |
| GET | /api/products | List active products |
| GET | /api/products/{id} | Get product |
| PUT | /api/products/{id} | Update product |
| DELETE | /api/products/{id} | Soft delete |

## Error codes
- `PRODUCT_NOT_FOUND` (404)
- `DUPLICATE_SKU` (409)
- `VALIDATION_ERROR` (422)
