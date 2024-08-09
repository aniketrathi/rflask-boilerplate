from modules.application.repository import ApplicationRepository


class ExtractPurchaseOrderHistoryRequestRepository(ApplicationRepository):
    collection_name = "extract_purchase_order_history_requests"
