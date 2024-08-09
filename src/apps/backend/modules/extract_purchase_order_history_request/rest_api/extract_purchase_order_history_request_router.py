from flask import Blueprint

from modules.extract_purchase_order_history_request.rest_api.extract_purchase_order_history_request_view import (
    ExtractPurchaseOrderHistoryRequestView,
)


class ExtractPurchaseOrderHistoryRequestRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        extract_purchase_order_history_request_view = ExtractPurchaseOrderHistoryRequestView()

        blueprint.add_url_rule(
            "",
            view_func=extract_purchase_order_history_request_view.create_extract_purchase_order_history_request,
            methods=["POST"],
        )

        return blueprint
