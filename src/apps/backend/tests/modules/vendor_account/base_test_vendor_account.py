import unittest
from typing import Callable

from modules.vendor_account.internal.store.vendor_account_repository import VendorAccountRepository
from modules.vendor_account.rest_api.vendor_account_rest_api_server import VendorAccountRestApiServer
from modules.config.config_manager import ConfigManager
from modules.logger.logger_manager import LoggerManager
from modules.account.internal.store.account_repository import AccountRepository


class BaseTestVendorAccount(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        ConfigManager.mount_config()
        LoggerManager.mount_logger()
        VendorAccountRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        VendorAccountRepository.collection().delete_many({})
        AccountRepository.collection().delete_many({})
