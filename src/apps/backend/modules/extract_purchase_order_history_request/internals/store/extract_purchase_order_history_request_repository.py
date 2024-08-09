from modules.application.repository import ApplicationRepository


class ExtractPurchaseOrderHistoryRequestRepository(ApplicationRepository):
    collection_name = "extract_purchase_order_history_requests"

    @classmethod
    def on_init_collection(cls, collection):
        collection.create_index("vendor_account_id")
