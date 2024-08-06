from bson import ObjectId

from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.types import VendorAccount
from modules.vendor_account.internal.vendor_account_util import VendorAccountUtil


class VendorAccountReader:
    @staticmethod
    def get_vendor_account_optional(account_id: str, vendor_account_name: str) -> VendorAccount:
        vendor_account_db = VendorAccountRepository.collection().find_one(
            {"account": ObjectId(account_id), "name": vendor_account_name, "active": True}
        )

        if vendor_account_db:
            return VendorAccountUtil.convert_vendor_account_db_to_vendor_account(vendor_account_db=vendor_account_db)
