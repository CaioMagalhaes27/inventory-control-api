# Stockwise frontend

Single-page dashboard for the Inventory Control API. Vanilla **HTML + CSS + JavaScript** — no build step, no framework.

## What it does

- **Dashboard** — four metric cards (Total Products, Stock Items, Low Stock, Expiring) plus recent activity widgets.
- **Products** — catalog table + creation form.
- **Stock Items** — items table + creation form. Copy any id to the clipboard with one click.
- **Movements** — entry and exit forms with a quick stock reference table.
- **Alerts** — visual cards for low stock and items expiring within 30 days.

Loading, error, empty and success states are handled across every view (toast notifications, inline form messages, empty-state placeholders).

## Architecture

| File           | Role                                                                              |
|----------------|-----------------------------------------------------------------------------------|
| `index.html`   | Markup for the sidebar + five views.                                              |
| `styles.css`   | Design system (CSS variables, typography, layout, components).                    |
| `app.js`       | Vanilla SPA. Fetches data, renders, wires forms.                                  |
| `serve.py`     | Static server on port 3000 that also reverse-proxies `/api/*` to the backends.    |

`app.js` calls the API using relative paths (`/api/products`, `/api/stock-items`). `serve.py` forwards those to:

- `http://localhost:8081` (product-service)
- `http://localhost:8082` (inventory-service)

This avoids CORS configuration on the backends and keeps everything single-origin.

## Run locally (backend already running)

Boot the backends in another terminal — either with `uvicorn` or `docker compose up -d` (see the repo root README).

Then start the frontend:

```bash
python frontend/serve.py
# Stockwise frontend listening on http://0.0.0.0:3000
```

Open <http://localhost:3000>.

### Overriding the backend URLs

```bash
PRODUCT_API=http://localhost:9001 \
INVENTORY_API=http://localhost:9002 \
python frontend/serve.py --port 3000
```

## Endpoints consumed

| Method | Path                                       | Backend              |
|--------|--------------------------------------------|----------------------|
| GET    | `/api/products`                            | product-service      |
| POST   | `/api/products`                            | product-service      |
| GET    | `/api/stock-items`                         | inventory-service    |
| POST   | `/api/stock-items`                         | inventory-service    |
| POST   | `/api/stock-items/{id}/entries`            | inventory-service    |
| POST   | `/api/stock-items/{id}/exits`              | inventory-service    |
| GET    | `/api/stock-items/low-stock`               | inventory-service    |
| GET    | `/api/stock-items/expiring`                | inventory-service    |

## Visual

- Light gray canvas, white sidebar, teal/green active state.
- Display typeface: `Instrument Serif` for headings and metric numbers.
- Body typeface: `Plus Jakarta Sans`. Mono details in `JetBrains Mono`.
- Rounded buttons (`pill` radius) and subtle gradient accents on primary actions.
- Live API status indicator pulses green when both services answer.

## Browser support

Modern evergreen browsers (Chrome, Firefox, Edge, Safari). Uses `fetch`, `Promise`, `FormData`, `Clipboard API`. No polyfills shipped.
