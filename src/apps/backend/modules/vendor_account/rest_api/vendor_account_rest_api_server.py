from flask import Blueprint

from modules.vendor_account.rest_api.vendor_account_router import VendorAccountRouter


class VendorAccountRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        vendor_account_api_blueprint = Blueprint("vendor_account", __name__)
        return VendorAccountRouter.create_route(blueprint=vendor_account_api_blueprint)
