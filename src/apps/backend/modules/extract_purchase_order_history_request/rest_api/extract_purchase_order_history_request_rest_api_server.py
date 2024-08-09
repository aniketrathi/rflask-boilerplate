from flask import Blueprint

from modules.extract_purchase_order_history_request.rest_api.extract_purchase_order_history_request_router import (
    ExtractPurchaseOrderHistoryRequestRouter,
)


class ExtractPurchaseOrderHistoryRequestRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        extract_purchase_order_history_request_api_blueprint = Blueprint(
            "extract_purchase_order_history_request",
            __name__,
            url_prefix="/accounts/<account_id>/vendor-accounts/<vendor_account_id>/extract-purchase-order-history-requests",
        )
        return ExtractPurchaseOrderHistoryRequestRouter.create_route(
            blueprint=extract_purchase_order_history_request_api_blueprint
        )
