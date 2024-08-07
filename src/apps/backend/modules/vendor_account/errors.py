from modules.error.custom_errors import AppError
from modules.vendor_account.types import VendorAccountErrorCode


class VendorAccountWithSameNameAndAccountExistsError(AppError):
    def __init__(self, vendor_account_name: str) -> None:
        message = f"A vendor account with the name {vendor_account_name} has already been created. Please choose a different name."
        super().__init__(code=VendorAccountErrorCode.NAME_ALREADY_EXISTS, https_status_code=409, message=message)


class VendorAccountNotFoundError(AppError):
    def __init__(self, vendor_account_id: str) -> None:
        message = f"Vendor account with id {vendor_account_id} not found. Please verify the id and try again."
        super().__init__(code=VendorAccountErrorCode.VENDOR_ACCOUNT_NOT_FOUND, https_status_code=404, message=message)
