import json
from unittest.mock import patch

from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import CreateAccessTokenParams
from modules.account.account_service import AccountService
from modules.account.types import CreateAccountParams
from modules.extract_purchase_order_history_request.types import ExtractPurchaseOrderHistoryRequestStatus
from modules.vendor_account.types import CreateVendorAccountParams
from modules.vendor_account.vendor_account_service import VendorAccountService
from server import app
from tests.modules.extract_purchase_order_history_request.base_test_extract_purchase_order_history_request import (
    BaseTestExtractPurchaseOrderHistoryRequest,
)


class TestExtractPurchaseOrderHistoryRequestApi(BaseTestExtractPurchaseOrderHistoryRequest):
    def setUp(self):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )
        self.account_id = account.id

        access_token = AccessTokenService.create_access_token(
            params=CreateAccessTokenParams(username=account.username, password="password")
        )
        self.access_token = access_token.token

        vendor_account = VendorAccountService.create_vendor_account(
            params=CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")
        )
        self.vendor_account_id = vendor_account.id

    def test_create_vendor_account(self) -> None:
        payload = json.dumps({"password": "amz-01#test", "username": "test@test.com"})

        with app.test_client() as client:
            response = client.post(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/{self.vendor_account_id}/extract-purchase-order-history-requests",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=payload,
            )
            assert response.status_code == 201
            assert response.json, f"No response from API with status code:: {response.status}"
            assert response.json.get("status") == ExtractPurchaseOrderHistoryRequestStatus.QUEUED.value
            assert response.json.get("vendor_account_id") == self.vendor_account_id

    @patch("subprocess.Popen")
    def test_amazon_purchase_order_history_extraction_worker_is_queued(self, mock_popen) -> None:
        payload = json.dumps({"password": "amz-01#test", "username": "test@test.com"})

        with app.test_client() as client:
            response = client.post(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/{self.vendor_account_id}/extract-purchase-order-history-requests",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=payload,
            )

        expected_command = f"npm run run:amazon-purchase-order-history-extraction --username=test@test.com --password=amz-01#test --request_id={response.json["id"]}"
        mock_popen.assert_called_once_with(expected_command, shell=True)
