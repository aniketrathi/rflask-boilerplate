import unittest
from typing import Callable

from modules.account.internal.store.account_repository import AccountRepository
from modules.config.config_manager import ConfigManager
from modules.extract_purchase_order_history_request.rest_api.extract_purchase_order_history_request_rest_api_server import (
    ExtractPurchaseOrderHistoryRequestRestApiServer,
)
from modules.logger.logger_manager import LoggerManager
from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository


class BaseTestExtractPurchaseOrderHistoryRequest(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        ConfigManager.mount_config()
        LoggerManager.mount_logger()
        ExtractPurchaseOrderHistoryRequestRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        AccountRepository.collection().delete_many({})
        VendorAccountRepository.collection().delete_many({})
