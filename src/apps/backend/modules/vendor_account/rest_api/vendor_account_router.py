from flask import Blueprint

from modules.vendor_account.rest_api.vendor_account_view import VendorAccountView


class VendorAccountRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        vendor_account_view = VendorAccountView()

        blueprint.add_url_rule("", view_func=vendor_account_view.create_vendor_account, methods=["POST"])

        blueprint.add_url_rule(
            "/<vendor_account_id>", view_func=vendor_account_view.update_vendor_account, methods=["PUT"]
        )

        blueprint.add_url_rule(
            "/<vendor_account_id>", view_func=vendor_account_view.delete_vendor_account, methods=["DELETE"]
        )

        blueprint.add_url_rule("", view_func=vendor_account_view.get_vendor_accounts, methods=["GET"])
        return blueprint
