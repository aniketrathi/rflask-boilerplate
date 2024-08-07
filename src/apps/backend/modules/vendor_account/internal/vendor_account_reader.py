from typing import List
from bson import ObjectId
from pymongo import ASCENDING

from modules.vendor_account.errors import VendorAccountNotFoundError
from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.types import VendorAccount, VendorType
from modules.vendor_account.internal.vendor_account_util import VendorAccountUtil


class VendorAccountReader:
    @staticmethod
    def get_vendor_account_optional(
        account_id: str, vendor_account_name: str, vendor_type: VendorType
    ) -> VendorAccount:
        vendor_account_db = VendorAccountRepository.collection().find_one(
            {
                "account_id": ObjectId(account_id),
                "active": True,
                "name": vendor_account_name,
                "vendor_type": vendor_type,
            }
        )

        if vendor_account_db:
            return VendorAccountUtil.convert_vendor_account_db_to_vendor_account(vendor_account_db=vendor_account_db)

    @staticmethod
    def get_vendor_account_by_id(account_id: str, vendor_account_id: str) -> VendorAccount:
        vendor_account_db = VendorAccountRepository.collection().find_one(
            {"account_id": ObjectId(account_id), "active": True, "_id": ObjectId(vendor_account_id)}
        )

        if vendor_account_db is None:
            raise VendorAccountNotFoundError(vendor_account_id=vendor_account_id)

        return VendorAccountUtil.convert_vendor_account_db_to_vendor_account(vendor_account_db=vendor_account_db)

    @staticmethod
    def get_vendor_accounts_by_account_id(account_id: str) -> List[VendorAccount]:
        vendor_accounts_db = (
            VendorAccountRepository.collection()
            .find({"account_id": ObjectId(account_id), "active": True})
            .sort([("name", ASCENDING), ("created_at", ASCENDING)])
        )

        return list(map(VendorAccountUtil.convert_vendor_account_db_to_vendor_account, vendor_accounts_db))
