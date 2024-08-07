from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.vendor_account.vendor_account_service import VendorAccountService
from modules.vendor_account.types import CreateVendorAccountParams, DeleteVendorAccountParams, UpdateVendorAccountParams
from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware


class VendorAccountView(MethodView):
    @access_auth_middleware
    def create_vendor_account(self, account_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        request_data["account_id"] = account_id
        vendor_account_params = CreateVendorAccountParams(**request_data)
        vendor_account = VendorAccountService.create_vendor_account(params=vendor_account_params)
        vendor_account_dict = asdict(vendor_account)
        return jsonify(vendor_account_dict), 201

    @access_auth_middleware
    def update_vendor_account(self, account_id: str, vendor_account_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        request_data["account_id"] = account_id
        request_data["vendor_account_id"] = vendor_account_id
        vendor_account = VendorAccountService.update_vendor_account(params=UpdateVendorAccountParams(**request_data))
        vendor_account_dict = asdict(vendor_account)
        return jsonify(vendor_account_dict), 200

    @access_auth_middleware
    def delete_vendor_account(self, account_id: str, vendor_account_id: str) -> ResponseReturnValue:
        VendorAccountService.delete_vendor_account(
            params=DeleteVendorAccountParams(account_id=account_id, vendor_account_id=vendor_account_id)
        )
        return jsonify(), 204

    @access_auth_middleware
    def get_vendor_accounts(self, account_id: str) -> ResponseReturnValue:
        vendor_accounts = VendorAccountService.get_vendor_accounts(account_id=account_id)
        vendor_accounts_list = list(map(asdict, vendor_accounts))
        return jsonify(vendor_accounts_list), 200
