from modules.vendor_account.types import CreateVendorAccountParams, VendorAccount
from modules.vendor_account.internal.vendor_account_writer import VendorAccountWriter


class VendorAccountService:
    @staticmethod
    def create_vendor_account(params: CreateVendorAccountParams) -> VendorAccount:
        return VendorAccountWriter.create_vendor_account(params=params)
