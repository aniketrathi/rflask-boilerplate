import subprocess

from modules.extract_purchase_order_history_request.internals.extract_purchase_order_history_request_reader import (
    ExtractPurchaseOrderHistoryRequestReader,
)
from modules.extract_purchase_order_history_request.internals.extract_purchase_order_history_request_writer import (
    ExtractPurchaseOrderHistoryRequestWriter,
)
from modules.extract_purchase_order_history_request.types import (
    ExtractPurchaseOrderHistoryParams,
    ExtractPurchaseOrderHistoryRequest,
    GetExtractPurchaseOrderHistoryRequesParams,
)
from modules.vendor_account.vendor_account_service import VendorAccountService


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

    @staticmethod
    def get_extract_purchase_order_history_request(
        params: GetExtractPurchaseOrderHistoryRequesParams,
    ) -> ExtractPurchaseOrderHistoryRequest:
        VendorAccountService.get_vendor_account(
            account_id=params.account_id, vendor_account_id=params.vendor_account_id
        )
        return ExtractPurchaseOrderHistoryRequestReader.get_extract_purchase_order_history_request_by_id(
            request_id=params.extract_purchase_order_history_request_id, vendor_account_id=params.vendor_account_id
        )
