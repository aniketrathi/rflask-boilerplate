from pymongo import ASCENDING
from modules.application.repository import ApplicationRepository


class VendorAccountRepository(ApplicationRepository):
    collection_name = "vendor_accounts"

    @classmethod
    def on_init_collection(cls, collection):
        collection.create_index([("account_id", ASCENDING), ("active", ASCENDING), ("name", ASCENDING)])
