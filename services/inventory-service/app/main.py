from fastapi import FastAPI

from app.presentation.exception_handlers.handlers import register_exception_handlers
from app.presentation.routers.stock_router import router as stock_router


def create_app() -> FastAPI:
    app = FastAPI(title="inventory-service", version="1.0.0")
    register_exception_handlers(app)
    app.include_router(stock_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": "inventory-service"}

    return app


app = create_app()
