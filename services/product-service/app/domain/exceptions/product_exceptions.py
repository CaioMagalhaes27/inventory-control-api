class DomainError(Exception):
    code: str = "DOMAIN_ERROR"
    status_code: int = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ProductNotFoundError(DomainError):
    code = "PRODUCT_NOT_FOUND"
    status_code = 404

    def __init__(self, product_id: str):
        super().__init__(f"Product with id '{product_id}' not found")


class DuplicateSkuError(DomainError):
    code = "DUPLICATE_SKU"
    status_code = 409

    def __init__(self, sku: str):
        super().__init__(f"Product with sku '{sku}' already exists")


class ValidationError(DomainError):
    code = "VALIDATION_ERROR"
    status_code = 422

    def __init__(self, message: str):
        super().__init__(message)
