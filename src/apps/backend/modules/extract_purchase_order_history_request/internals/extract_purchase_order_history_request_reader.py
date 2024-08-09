from bson import ObjectId

from modules.extract_purchase_order_history_request.errors import ExtractPurchaseOrderHistoryRequestNotFoundError
from modules.extract_purchase_order_history_request.internals.extract_purchase_order_history_request_util import (
    ExtractPurchaseOrderHistoryRequestUtil,
)
from modules.extract_purchase_order_history_request.internals.store.extract_purchase_order_history_request_repository import (
    ExtractPurchaseOrderHistoryRequestRepository,
)
from modules.extract_purchase_order_history_request.types import ExtractPurchaseOrderHistoryRequest


class ExtractPurchaseOrderHistoryRequestReader:
    @staticmethod
    def get_extract_purchase_order_history_request_by_id(request_id: str) -> ExtractPurchaseOrderHistoryRequest:
        extract_purchase_order_history_request_db = ExtractPurchaseOrderHistoryRequestRepository.collection().find_one(
            {"_id": ObjectId(request_id)}
        )

        if extract_purchase_order_history_request_db is None:
            raise ExtractPurchaseOrderHistoryRequestNotFoundError(request_id=request_id)

        return ExtractPurchaseOrderHistoryRequestUtil.convert_extract_purchase_order_history_request_db_to_extract_purchase_order_history_request(
            extract_purchase_order_history_request_db=extract_purchase_order_history_request_db
        )
