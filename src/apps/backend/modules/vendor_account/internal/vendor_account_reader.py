from modules.vendor_account.errors import VendorAccountWithSameNameAndAccountExistsError
from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.types import NameAlreadyExistParams, VendorAccount


class VendorAccountReader:
    @staticmethod
    def check_name_not_exist(params: NameAlreadyExistParams) -> VendorAccount:
        vendor_account = VendorAccountRepository.collection().find_one(
            {"account": params.account_id, "name": params.name, "active": True}
        )

        if vendor_account:
            raise VendorAccountWithSameNameAndAccountExistsError(
                f"Vendor account with name {params.name} already exist"
            )
