from dataclasses import dataclass
from enum import Enum


class VendorType(Enum):
    AMAZON = "AMAZON"

@dataclass(frozen=True)
class VendorAccount:
    account_id: str
    id: str
    name: str
    vendor_type: VendorType

@dataclass(frozen=True)
class CreateVendorAccountParams:
    account_id: str
    name: str
    vendor_type: VendorType


@dataclass(frozen=True)
class VendorAccountErrorCode:
    NAME_ALREADY_EXISTS: str = "VENDOR_ACCOUNT_ERR_01"
