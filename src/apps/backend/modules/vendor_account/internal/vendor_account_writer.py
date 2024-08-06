from bson import ObjectId
from datetime import datetime, timezone

from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.internal.vendor_account_reader import VendorAccountReader
from modules.vendor_account.internal.vendor_account_util import VendorAccountUtil
from modules.vendor_account.types import CreateVendorAccountParams
from modules.vendor_account.types import VendorAccount
from modules.vendor_account.errors import VendorAccountWithSameNameAndAccountExistsError


class VendorAccountWriter:
    @staticmethod
    def create_vendor_account(params: CreateVendorAccountParams) -> VendorAccount:
        vendor_account = VendorAccountReader.get_vendor_account_optional(
            account_id=params.account_id, vendor_account_name=params.name
        )

        if vendor_account:
            raise VendorAccountWithSameNameAndAccountExistsError(vendor_account_name=params.name)

        vendor_account_data = {
            "account": ObjectId(params.account_id),
            "active": True,
            "created_at": datetime.now(timezone.utc),
            "name": params.name,
            "updated_at": datetime.now(timezone.utc),
            "vendor_type": params.vendor_type,
        }

        result = VendorAccountRepository.collection().insert_one(vendor_account_data)
        vendor_account_db = VendorAccountRepository.collection().find_one({"_id": result.inserted_id})
        return VendorAccountUtil.convert_vendor_account_db_to_vendor_account(vendor_account_db=vendor_account_db)
