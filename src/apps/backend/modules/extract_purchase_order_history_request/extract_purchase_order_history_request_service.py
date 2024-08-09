import subprocess

from modules.extract_purchase_order_history_request.internals.extract_purchase_order_history_request_writer import (
    ExtractPurchaseOrderHistoryRequestWriter,
)
from modules.extract_purchase_order_history_request.types import (
    ExtractPurchaseOrderHistoryParams,
    ExtractPurchaseOrderHistoryRequest,
)


class PurchaseOrderHistorySerivce:
    @staticmethod
    def extract_purchase_order_history(params: ExtractPurchaseOrderHistoryParams) -> ExtractPurchaseOrderHistoryRequest:
        extract_purchase_order_history_request = (
            ExtractPurchaseOrderHistoryRequestWriter.create_extract_purchase_order_history_request(
                vendor_account_id=params.vendor_account_id
            )
        )

        # Run the worker with username, password, and request ID in the background
        command = f"npm run run:amazon-purchase-order-history-extraction --username={params.vendor_account_username} --password={params.vendor_account_password} --request_id={extract_purchase_order_history_request.id}"
        subprocess.Popen(command, shell=True)

        return extract_purchase_order_history_request
