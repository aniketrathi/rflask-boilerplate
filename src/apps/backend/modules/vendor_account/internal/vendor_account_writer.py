from datetime import datetime, timezone

from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.internal.vendor_account_reader import VendorAccountReader
from modules.vendor_account.internal.vendor_account_util import VendorAccountUtil
from modules.vendor_account.types import CreateVendorAccountParams, NameAlreadyExistParams


class VendorAccountWriter:
    @staticmethod
    def create_vendor_account(params: CreateVendorAccountParams):
        VendorAccountReader.check_name_not_exist(
            params=NameAlreadyExistParams(account_id=params.account_id, name=params.name)
        )

        vendor_account_data = {
            "account": params.account_id,
            "name": params.name,
            "vendor_type": params.vendor_type,
            "active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        result = VendorAccountRepository.collection().insert_one(vendor_account_data)
        vendor_account_db = VendorAccountRepository.collection().find_one({"_id": result.inserted_id})
        return VendorAccountUtil.convert_vendor_account_db_to_vendor_account(vendor_account_db=vendor_account_db)
