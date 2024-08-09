from typing import Dict

from modules.extract_purchase_order_history_request.types import ExtractPurchaseOrderHistoryRequest


class ExtractPurchaseOrderHistoryRequestUtil:
    @staticmethod
    def convert_extract_purchase_order_history_request_db_to_extract_purchase_order_history_request(
        extract_purchase_order_history_request_db: Dict,
    ) -> ExtractPurchaseOrderHistoryRequest:
        return ExtractPurchaseOrderHistoryRequest(
            id=str(extract_purchase_order_history_request_db["_id"]),
            status=extract_purchase_order_history_request_db["status"],
            two_factor_authentication_code=extract_purchase_order_history_request_db.get(
                "extract_purchase_order_history_request_db"
            ),
            user_display_message=extract_purchase_order_history_request_db.get("user_display_message"),
            vendor_account_id=str(extract_purchase_order_history_request_db["vendor_account_id"]),
        )
