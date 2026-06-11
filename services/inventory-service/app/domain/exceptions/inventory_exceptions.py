class DomainError(Exception):
    code: str = "DOMAIN_ERROR"
    status_code: int = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class StockItemNotFoundError(DomainError):
    code = "STOCK_ITEM_NOT_FOUND"
    status_code = 404

    def __init__(self, stock_item_id: str):
        super().__init__(f"Stock item with id '{stock_item_id}' not found")


class InsufficientStockError(DomainError):
    code = "INSUFFICIENT_STOCK"
    status_code = 409

    def __init__(self, available: int, requested: int):
        super().__init__(
            f"Insufficient stock: available={available}, requested={requested}"
        )


class ValidationError(DomainError):
    code = "VALIDATION_ERROR"
    status_code = 422

    def __init__(self, message: str):
        super().__init__(message)
