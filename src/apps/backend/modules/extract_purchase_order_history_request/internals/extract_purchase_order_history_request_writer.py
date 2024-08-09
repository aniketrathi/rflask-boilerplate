from bson import ObjectId

from modules.extract_purchase_order_history_request.internals.extract_purchase_order_history_request_util import (
    ExtractPurchaseOrderHistoryRequestUtil,
)
from modules.extract_purchase_order_history_request.internals.store.extract_purchase_order_history_request_repository import (
    ExtractPurchaseOrderHistoryRequestRepository,
)
from modules.extract_purchase_order_history_request.types import (
    ExtractPurchaseOrderHistoryRequest,
    ExtractPurchaseOrderHistoryRequestStatus,
)


class ExtractPurchaseOrderHistoryRequestWriter:
    @staticmethod
    def create_extract_purchase_order_history_request(vendor_account_id: str) -> ExtractPurchaseOrderHistoryRequest:
        result = ExtractPurchaseOrderHistoryRequestRepository.collection().insert_one(
            {
                "status": ExtractPurchaseOrderHistoryRequestStatus.QUEUED.value,
                "vendor_account_id": ObjectId(vendor_account_id),
            }
        )

        extract_purchase_order_history_request_db = ExtractPurchaseOrderHistoryRequestRepository.collection().find_one(
            {"_id": result.inserted_id}
        )

        return ExtractPurchaseOrderHistoryRequestUtil.convert_extract_purchase_order_history_request_db_to_extract_purchase_order_history_request(
            extract_purchase_order_history_request_db=extract_purchase_order_history_request_db
        )
