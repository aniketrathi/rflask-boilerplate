from bson import ObjectId

from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.account.account_service import AccountService
from modules.account.types import CreateAccountParams
from modules.vendor_account.vendor_account_service import VendorAccountService
from modules.vendor_account.errors import VendorAccountNotFoundError, VendorAccountWithSameNameAndAccountExistsError
from modules.vendor_account.types import (
    DeleteVendorAccountParams,
    UpdateVendorAccountParams,
    VendorAccountErrorCode,
    CreateVendorAccountParams,
)
from tests.modules.vendor_account.base_test_vendor_account import BaseTestVendorAccount


class TestVendorAccountService(BaseTestVendorAccount):
    def setUp(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        self.account_id = account.id

    def test_create_vendor_account(self) -> None:
        vendor_account = VendorAccountService.create_vendor_account(
            params=CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")
        )

        assert vendor_account.account_id == self.account_id
        assert vendor_account.name == "Amz-01"
        assert vendor_account.vendor_type == "AMAZON"

    def test_throw_exception_when_vendor_account_with_same_name_account_and_vendor_type_exist(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        try:
            VendorAccountService.create_vendor_account(params)
        except VendorAccountWithSameNameAndAccountExistsError as exc:
            assert exc.code == VendorAccountErrorCode.NAME_ALREADY_EXISTS

    def test_update_vendor_account(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        vendor_account = VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        update_vendor_account = VendorAccountService.update_vendor_account(
            params=UpdateVendorAccountParams(
                account_id=self.account_id, vendor_account_id=vendor_account.id, name="Amz-02"
            )
        )

        assert update_vendor_account.account_id == self.account_id
        assert update_vendor_account.id == vendor_account.id
        assert update_vendor_account.name == "Amz-02"
        assert update_vendor_account.vendor_type == "AMAZON"

    def test_throw_exception_when_vendor_account_does_not_exist_while_updating_vendor_account(self) -> None:
        try:
            VendorAccountService.update_vendor_account(
                params=UpdateVendorAccountParams(
                    account_id=self.account_id, vendor_account_id="66b2400af6d99e62d6e7992c", name="Amz-02"
                )
            )
        except VendorAccountNotFoundError as exc:
            assert exc.code == VendorAccountErrorCode.VENDOR_ACCOUNT_NOT_FOUND

    def test_delete_vendor_account(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        vendor_account = VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        vendor_account_before = VendorAccountRepository.collection().find_one({"_id": ObjectId(vendor_account.id)})
        assert vendor_account_before["active"] == True

        VendorAccountService.delete_vendor_account(
            params=DeleteVendorAccountParams(account_id=self.account_id, vendor_account_id=vendor_account.id)
        )

        vendor_account_after = VendorAccountRepository.collection().find_one({"_id": ObjectId(vendor_account.id)})
        assert vendor_account_after["active"] == False

    def test_throw_exception_when_vendor_account_does_not_exist_while_deleting_vendor_account(self) -> None:
        try:
            VendorAccountService.delete_vendor_account(
                params=DeleteVendorAccountParams(
                    account_id=self.account_id, vendor_account_id="66b2400af6d99e62d6e7992c"
                )
            )
        except VendorAccountNotFoundError as exc:
            assert exc.code == VendorAccountErrorCode.VENDOR_ACCOUNT_NOT_FOUND

    def test_get_all_vendor_accounts(self) -> None:
        # Pre test setup
        params_one = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params_one)

        params_two = CreateVendorAccountParams(account_id=self.account_id, name="Amz-02", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params_two)
        # Pre test setup end

        vendor_accounts = VendorAccountService.get_vendor_accounts(account_id=self.account_id)

        assert len(vendor_accounts) == 2
        assert vendor_accounts[0].account_id == self.account_id
        assert vendor_accounts[0].name == "Amz-01"
        assert vendor_accounts[0].vendor_type == "AMAZON"
        assert vendor_accounts[1].account_id == self.account_id
        assert vendor_accounts[1].name == "Amz-02"
        assert vendor_accounts[1].vendor_type == "AMAZON"
