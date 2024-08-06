from modules.error.custom_errors import AppError
from modules.vendor_account.types import VendorAccountErrorCode


class VendorAccountWithSameNameAndAccountExistsError(AppError):
    def __init__(self, vendor_account_name: str) -> None:
        print(vendor_account_name);
        message = f"A vendor account with the name {vendor_account_name} has already been created. Please choose a different name."
        super().__init__(code=VendorAccountErrorCode.NAME_ALREADY_EXISTS, https_status_code=409, message=message)
