from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.vendor_account.vendor_account_service import VendorAccountService
from modules.vendor_account.types import CreateVendorAccountParams
from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware


class VendorAccountView(MethodView):
    @access_auth_middleware
    def post(self, account_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        request_data['account_id'] = account_id 
        vendor_account_params = CreateVendorAccountParams(**request_data)
        vendor_account = VendorAccountService.create_vendor_account(params=vendor_account_params)
        vendor_account_dict = asdict(vendor_account)
        return jsonify(vendor_account_dict), 201
