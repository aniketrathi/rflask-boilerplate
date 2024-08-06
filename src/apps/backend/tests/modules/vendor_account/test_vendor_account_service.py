from modules.account.account_service import AccountService
from modules.account.types import CreateAccountParams
from modules.vendor_account.vendor_account_service import VendorAccountService
from modules.vendor_account.errors import VendorAccountWithSameNameAndAccountExistsError
from modules.vendor_account.types import VendorAccountErrorCode, CreateVendorAccountParams
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

        assert vendor_account.account == self.account_id
        assert vendor_account.name == "Amz-01"
        assert vendor_account.vendor_type == "AMAZON"

    def test_throw_exception_when_vendor_account_with_same_name_and_account_exist(self) -> None:
        # Pre test setup
        params = CreateVendorAccountParams(account_id=self.account_id, name="Amz-01", vendor_type="AMAZON")

        VendorAccountService.create_vendor_account(params)
        # Pre test setup end

        try:
            VendorAccountService.create_vendor_account(params)
        except VendorAccountWithSameNameAndAccountExistsError as exc:
            assert exc.code == VendorAccountErrorCode.NAME_ALREADY_EXISTS
