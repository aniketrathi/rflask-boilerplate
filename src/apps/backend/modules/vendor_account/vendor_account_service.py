from modules.vendor_account.types import (
    CreateVendorAccountParams,
    DeleteVendorAccountParams,
    UpdateVendorAccountParams,
    VendorAccount,
)
from modules.vendor_account.internal.vendor_account_writer import VendorAccountWriter


class VendorAccountService:
    @staticmethod
    def create_vendor_account(params: CreateVendorAccountParams) -> VendorAccount:
        return VendorAccountWriter.create_vendor_account(params=params)

    @staticmethod
    def update_vendor_account(params: UpdateVendorAccountParams) -> VendorAccount:
        return VendorAccountWriter.update_vendor_account(params=params)

    @staticmethod
    def delete_vendor_account(params: DeleteVendorAccountParams) -> None:
        return VendorAccountWriter.delete_vendor_account(params=params)
