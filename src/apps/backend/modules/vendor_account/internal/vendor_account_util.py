from typing import Dict

from modules.vendor_account.types import VendorAccount


class VendorAccountUtil:
    @staticmethod
    def convert_vendor_account_db_to_vendor_account(vendor_account_db: Dict) -> VendorAccount:
        return VendorAccount(
            account_id=str(vendor_account_db["account_id"]),
            id=str(vendor_account_db["_id"]),
            name=vendor_account_db["name"],
            vendor_type=vendor_account_db["vendor_type"],
        )
