import json

from modules.account.types import CreateAccountParams
from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import CreateAccessTokenParams
from modules.account.account_service import AccountService
from modules.vendor_account.vendor_account_service import VendorAccountService
from modules.vendor_account.types import VendorAccountErrorCode, CreateVendorAccountParams
from server import app
from tests.modules.vendor_account.base_test_vendor_account import BaseTestVendorAccount


class TestVendorAccountApi(BaseTestVendorAccount):
    def setUp(self):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        access_token = AccessTokenService.create_access_token(
            params=CreateAccessTokenParams(username=account.username, password="password")
        )

        self.account_id = account.id
        self.access_token = access_token.token


    def test_create_vendor_account(self) -> None:
        payload = json.dumps({"name": "Amz-01", "vendor_type": "AMAZON"})

        with app.test_client() as client:
            response = client.post(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=payload,
            )
            assert response.status_code == 201
            assert response.json, f"No response from API with status code:: {response.status}"
            assert response.json.get("account_id") == self.account_id
            assert response.json.get("name") == "Amz-01"
            assert response.json.get("vendor_type") == "AMAZON"

    def test_create_vendor_account_with_same_account_name_and_vendor_type(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        with app.test_client() as client:
            response = client.post(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=json.dumps({"name": "Amz-01", "vendor_type": "AMAZON"}),
            )
        assert response.status_code == 409
        assert response.json
        assert response.json.get("code") == VendorAccountErrorCode.NAME_ALREADY_EXISTS
        assert response.json.get("message") == f"A vendor account with the name {params.name} has already been created. Please choose a different name."

    def test_create_vendor_account_with_same_account_and_name_but_for_different_vendor(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Vendor-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        with app.test_client() as client:
            response = client.post(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=json.dumps({"name": params.name, "vendor_type": "Croma"}),
            )
            assert response.status_code == 201
            assert response.json, f"No response from API with status code:: {response.status}"
            assert response.json.get("account_id") == self.account_id
            assert response.json.get("name") == params.name
            assert response.json.get("vendor_type") == "Croma"
