import os
import sys

# Add the parent directory to the system path to access modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from modules.config.config_manager import ConfigManager
from modules.logger.logger import Logger
from modules.logger.logger_manager import LoggerManager


def mount_dependencies() -> None:
    ConfigManager.mount_config()
    LoggerManager.mount_logger()


def run_amazon_purchase_order_history_extraction_worker(
    extract_purchase_order_history_request_id: str, password: str, username: str
) -> None:
    try:
        Logger.info(
            message=f"Amazon purchase order history extraction initiated for record: {extract_purchase_order_history_request_id}"
        )
        # Will add logic here
        sys.exit(0)
    except Exception as error:
        Logger.error(message=f"Error processing purchase order history extraction record: {error}")


if __name__ == "__main__":
    mount_dependencies()

    username = sys.argv[1]
    password = sys.argv[2]
    extract_purchase_order_history_request_id = sys.argv[3]

    if username is None:
        Logger.error(message="Error: username is required as a command line arguments.")
        sys.exit(1)

    if password is None:
        Logger.error(message="Error: password is required as a command line arguments.")
        sys.exit(1)

    if extract_purchase_order_history_request_id is None:
        Logger.error(
            message="Error: extract_purchase_order_history_request_id is required as a command line arguments."
        )
        sys.exit(1)

    try:
        run_amazon_purchase_order_history_extraction_worker(
            extract_purchase_order_history_request_id=extract_purchase_order_history_request_id,
            password=password,
            username=username,
        )
        sys.exit(0)
    except Exception as error:
        Logger.error(message=f"Error running purchase order history extraction worker: {error}")
