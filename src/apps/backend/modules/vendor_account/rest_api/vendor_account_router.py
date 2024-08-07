from flask import Blueprint

from modules.vendor_account.rest_api.vendor_account_view import VendorAccountView


class VendorAccountRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule(
            "/accounts/<account_id>/vendor-accounts", view_func=VendorAccountView.as_view("vendor_account_view")
        )

        blueprint.add_url_rule(
            "/accounts/<account_id>/vendor-accounts/<vendor_account_id>",
            view_func=VendorAccountView.as_view("vendor_account_update"),
            methods=["PUT"],
        )

        blueprint.add_url_rule(
            "/accounts/<account_id>/vendor-accounts/<vendor_account_id>",
            view_func=VendorAccountView.as_view("vendor_account_delete"),
            methods=["DELETE"],
        )
        return blueprint
