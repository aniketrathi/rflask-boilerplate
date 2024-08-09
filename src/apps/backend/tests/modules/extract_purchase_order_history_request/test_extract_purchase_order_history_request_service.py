from unittest.mock import patch

from modules.account.account_service import AccountService
from modules.account.types import CreateAccountParams
from modules.extract_purchase_order_history_request.extract_purchase_order_history_request_service import (
    PurchaseOrderHistorySerivce,
)
from modules.extract_purchase_order_history_request.types import (
    ExtractPurchaseOrderHistoryParams,
    ExtractPurchaseOrderHistoryRequestStatus,
)
from modules.vendor_account.types import CreateVendorAccountParams
from modules.vendor_account.vendor_account_service import VendorAccountService
from tests.modules.extract_purchase_order_history_request.base_test_extract_purchase_order_history_request import (
    BaseTestExtractPurchaseOrderHistoryRequest,
)


class TestExtractPurchaseOrderHistoryRequestService(BaseTestExtractPurchaseOrderHistoryRequest):
    def setUp(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )
        self.account_id = account.id

        vendor_account = VendorAccountService.create_vendor_account(
            params=CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")
        )
        self.vendor_account_id = vendor_account.id

    def test_create_extract_purchase_order_history_request(self) -> None:
        extract_purchase_order_history_request = PurchaseOrderHistorySerivce.extract_purchase_order_history(
            params=ExtractPurchaseOrderHistoryParams(
                vendor_account_id=self.vendor_account_id,
                vendor_account_password="#amz-01",
                vendor_account_username="test@test.com",
            )
        )

        assert extract_purchase_order_history_request.status == ExtractPurchaseOrderHistoryRequestStatus.QUEUED.value
        assert extract_purchase_order_history_request.vendor_account_id == self.vendor_account_id

    @patch("subprocess.Popen")
    def test_amazon_purchase_order_history_extraction_worker_is_queued(self, mock_popen) -> None:
        extract_purchase_order_history_params = ExtractPurchaseOrderHistoryParams(
            vendor_account_id=self.vendor_account_id,
            vendor_account_password="#amz-01",
            vendor_account_username="test@test.com",
        )
        extract_purchase_order_history_request = PurchaseOrderHistorySerivce.extract_purchase_order_history(
            params=extract_purchase_order_history_params
        )

        expected_command = f"npm run run:amazon-purchase-order-history-extraction --username={extract_purchase_order_history_params.vendor_account_username} --password={extract_purchase_order_history_params.vendor_account_password} --request_id={extract_purchase_order_history_request.id}"
        mock_popen.assert_called_once_with(expected_command, shell=True)
