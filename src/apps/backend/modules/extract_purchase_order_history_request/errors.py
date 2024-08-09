from modules.error.custom_errors import AppError
from modules.extract_purchase_order_history_request.types import ExtractPurchaseOrderHistoryRequestErrorCode


class ExtractPurchaseOrderHistoryRequestNotFoundError(AppError):
    def __init__(self, request_id: str) -> None:
        message = f"Extract purchase order history request with id {request_id} not found. Please verify the id and try again."
        super().__init__(
            code=ExtractPurchaseOrderHistoryRequestErrorCode.EXTRACT_PURCHASE_ORDER_HISTORY_REQUEST_NOT_FOUND,
            https_status_code=404,
            message=message,
        )
