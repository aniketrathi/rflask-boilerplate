from modules.error.custom_errors import AppError
from modules.vendor_account.types import VendorAccountErrorCode


class VendorAccountWithSameNameAndAccountExistsError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=VendorAccountErrorCode.NAME_ALREADY_EXISTS, https_status_code=409, message=message)
