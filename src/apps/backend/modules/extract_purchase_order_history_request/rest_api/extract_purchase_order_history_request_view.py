from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.extract_purchase_order_history_request.extract_purchase_order_history_request_service import (
    PurchaseOrderHistorySerivce,
)
from modules.extract_purchase_order_history_request.types import ExtractPurchaseOrderHistoryParams


class ExtractPurchaseOrderHistoryRequestView(MethodView):
    @access_auth_middleware
    def create_extract_purchase_order_history_request(
        self, account_id: str, vendor_account_id: str
    ) -> ResponseReturnValue:
        request_data = request.get_json()
        extract_purchase_order_history_params = ExtractPurchaseOrderHistoryParams(
            vendor_account_id=vendor_account_id,
            vendor_account_password=request_data["password"],
            vendor_account_username=request_data["username"],
        )
        extract_purchase_order_history_request = PurchaseOrderHistorySerivce.extract_purchase_order_history(
            params=extract_purchase_order_history_params
        )
        extract_purchase_order_history_request_dict = asdict(extract_purchase_order_history_request)
        return jsonify(extract_purchase_order_history_request_dict), 201

    def get_extract_purchase_order_history_request(
        self, account_id: str, vendor_account_id: str, extract_purchase_order_history_request_id: str
    ) -> ResponseReturnValue:
        extract_purchase_order_history_request = PurchaseOrderHistorySerivce.get_extract_purchase_order_history_request(
            request_id=extract_purchase_order_history_request_id
        )
        extract_purchase_order_history_request_dict = asdict(extract_purchase_order_history_request)
        return jsonify(extract_purchase_order_history_request_dict), 200
