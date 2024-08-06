from flask import Blueprint

from modules.vendor_account.rest_api.vendor_account_view import VendorAccountView


class VendorAccountRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/accounts/<account_id>/vendor-accounts", view_func=VendorAccountView.as_view("vendor_account_view"))
        return blueprint
