import json

from bson import ObjectId

from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import CreateAccessTokenParams
from modules.account.account_service import AccountService
from modules.account.types import CreateAccountParams
from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.types import CreateVendorAccountParams, VendorAccountErrorCode
from modules.vendor_account.vendor_account_service import VendorAccountService
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
        assert (
            response.json.get("message")
            == f"A vendor account with the name {params.name} has already been created. Please choose a different name."
        )

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

    def test_update_vendor_account(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        vendor_account = VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        with app.test_client() as client:
            response = client.put(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/{vendor_account.id}",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=json.dumps({"name": "Amz-01"}),
            )
            assert response.status_code == 200
            assert response.json, f"No response from API with status code:: {response.status}"
            assert response.json.get("account_id") == self.account_id
            assert response.json.get("id") == vendor_account.id
            assert response.json.get("name") == "Amz-01"
            assert response.json.get("vendor_type") == "AMAZON"

    def test_update_vendor_account_with_an_invalid_vendor_account_id(self) -> None:
        with app.test_client() as client:
            response = client.put(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/66b2400af6d99e62d6e7992c",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=json.dumps({"name": "Amz-01"}),
            )
        assert response.status_code == 404
        assert response.json
        assert response.json.get("code") == VendorAccountErrorCode.VENDOR_ACCOUNT_NOT_FOUND
        assert (
            response.json.get("message")
            == "Vendor account with id 66b2400af6d99e62d6e7992c not found. Please verify the id and try again."
        )

    def test_update_vendor_account_with_duplicate_name(self) -> None:
        # Pre test setup
        params_one = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params_one)

        params_two = CreateVendorAccountParams(account_id=self.account_id, name="Amz-02", vendor_type="AMAZON")

        vendor_account = VendorAccountService.create_vendor_account(params_two)
        # Pre test setup end

        with app.test_client() as client:
            response = client.put(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/{vendor_account.id}",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                data=json.dumps({"name": "Amz-01"}),
            )
        assert response.status_code == 409
        assert response.json
        assert response.json.get("code") == VendorAccountErrorCode.NAME_ALREADY_EXISTS
        assert (
            response.json.get("message")
            == f"A vendor account with the name {params_one.name} has already been created. Please choose a different name."
        )

    def test_delete_vendor_account(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        vendor_account = VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        vendor_account_before = VendorAccountRepository.collection().find_one({"_id": ObjectId(vendor_account.id)})
        assert vendor_account_before["active"] == True

        with app.test_client() as client:
            response = client.delete(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/{vendor_account.id}",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
            )
            assert response.status_code == 204

        vendor_account_after = VendorAccountRepository.collection().find_one({"_id": ObjectId(vendor_account.id)})
        assert vendor_account_after["active"] == False

    def test_delete_vendor_account_with_an_invalid_vendor_account_id(self) -> None:
        with app.test_client() as client:
            response = client.delete(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts/66b2400af6d99e62d6e7992c",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
            )
        assert response.status_code == 404
        assert response.json
        assert response.json.get("code") == VendorAccountErrorCode.VENDOR_ACCOUNT_NOT_FOUND
        assert (
            response.json.get("message")
            == "Vendor account with id 66b2400af6d99e62d6e7992c not found. Please verify the id and try again."
        )

    def test_get_all_vendor_accounts(self) -> None:
        # Pre test setup
        params_one = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params_one)

        params_two = CreateVendorAccountParams(account_id=self.account_id, name="Amz-02", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params_two)
        # Pre test setup end

        with app.test_client() as client:
            response = client.get(
                f"http://127.0.0.1:8080/api/accounts/{self.account_id}/vendor-accounts",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
            )

            assert response.status_code == 200
            assert response.json, f"No response from API with status code:: {response.status}"
            assert len(response.json) == 2
            assert response.json[0]["account_id"] == self.account_id
            assert response.json[0]["name"] == "Amz-01"
            assert response.json[0]["vendor_type"] == "AMAZON"
            assert response.json[1]["account_id"] == self.account_id
            assert response.json[1]["name"] == "Amz-02"
            assert response.json[1]["vendor_type"] == "AMAZON"
