from flask import Blueprint

from modules.vendor_account.rest_api.vendor_account_router import VendorAccountRouter


class VendorAccountRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        vendor_account_api_blueprint = Blueprint(
            "vendor_account", __name__, url_prefix="/accounts/<account_id>/vendor-accounts"
        )
        return VendorAccountRouter.create_route(blueprint=vendor_account_api_blueprint)
