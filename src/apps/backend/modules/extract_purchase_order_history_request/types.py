from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExtractPurchaseOrderHistoryRequestStatus(Enum):
    AWAITING_2FA_CODE = "AWAITING_2FA_CODE"
    AWAITING_2FA_CODE_VERIFICATION = "AWAITING_2FA_CODE_VERIFICATION"
    CREDENTIALS_VERIFICATION_IN_PROGRESS = "CREDENTIALS_VERIFICATION_IN_PROGRESS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    PURCHASE_ORDER_HISTORY_EXTRACTION_COMPLETED = "PURCHASE_ORDER_HISTORY_EXTRACTION_COMPLETED"
    PURCHASE_ORDER_HISTORY_EXTRACTION_IN_PROGRESS = "PURCHASE_ORDER_HISTORY_EXTRACTION_IN_PROGRESS"
    QUEUED = "QUEUED"


@dataclass(frozen=True)
class ExtractPurchaseOrderHistoryRequest:
    id: str
    status: ExtractPurchaseOrderHistoryRequestStatus
    vendor_account_id: str
    two_factor_authentication_code: Optional[str] = None
    user_display_message: Optional[str] = None


@dataclass(frozen=True)
class ExtractPurchaseOrderHistoryParams:
    vendor_account_id: str
    vendor_account_password: str
    vendor_account_username: str
