from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.exception_handlers.handlers import register_exception_handlers
from app.presentation.routers.product_router import router as product_router


def create_app() -> FastAPI:
    app = FastAPI(title="product-service", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    app.include_router(product_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": "product-service"}

    return app


app = create_app()
