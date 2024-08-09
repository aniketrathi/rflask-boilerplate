run-lint:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run mypy --config-file mypy.ini .

run-format:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run autoflake . -i \
	&& pipenv run isort . \
	&& pipenv run black .

run-vulture:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run vulture

run-engine:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run python --version \
	&& pipenv run gunicorn -c gunicorn_config.py server:app

run-test:
	cd src/apps/backend \
	&& pipenv install --dev \
	&& pipenv run pytest tests

run-engine-winx86:
	echo "This command is specifically for windows platform \
	sincas gunicorn is not well supported by windows os"
	cd src/apps/backend \
	&& pipenv install --dev && pipenv install \
	PYTHONPATH=./ pipenv run python scripts/$(file).py

run-amazon-purchase-order-history-extraction:
	cd src/apps/backend && \
	pipenv install --dev && \
	PYTHONPATH=./ pipenv run python modules/extract_purchase_order_history_request/workers/amazon_purchase_order_history_extraction_worker.py $(username) $(password) $(request_id)
