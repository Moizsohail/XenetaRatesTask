from flask import Flask
from logging import Formatter, FileHandler
from dataclasses import asdict
from accessors import improve_db, is_db_ready
from shared.constants import LOGGING_LEVEL
import services
from shared.specs import GetApiRatesParams, GetApiRatesQuery
from validators import (
    APIException,
    get_api_rates_query_validator,
)


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)
app.url_map.strict_slashes = False
with app.app_context():
    is_db_ready()
    improve_db()

file_handler = FileHandler("logs.log")
app.logger.setLevel(LOGGING_LEVEL)

file_handler.setLevel(LOGGING_LEVEL)
file_handler.setFormatter(
    Formatter(
        "%(asctime)s -"
        " %(funcName)s - %(levelname)s - %(message)s"
    )
)
app.logger.addHandler(file_handler)
app_logger = app.logger


# ----------------------------------------------------------------------------#
# Handlers.
# ----------------------------------------------------------------------------#


@app.route("/", methods=["GET"])
def home():
    return "Hello, World!"


@app.route("/rates", methods=["GET"])
@get_api_rates_query_validator
def get_api_rates_handler(spec: GetApiRatesQuery):

    spec = GetApiRatesParams(
        date_from=spec.date_from,
        date_to=spec.date_to,
        orig=spec.origin,
        dest=spec.destination,
    )

    prices = services.get_api_rates(spec)
    return [asdict(row) for row in prices]


# ----------------------------------------------------------------------------#
# Error handlers.
# ----------------------------------------------------------------------------#


@app.errorhandler(500)
def internal_error(error):
    return "Oh No, 500 Server Error!", 500


@app.errorhandler(APIException)
def handle_exception(err):
    """Return JSON instead of HTML for MyCustomError errors."""
    response = {
        "error": err.description,
    }
    if len(err.args) > 0:
        response["message"] = err.args[0]

    return response, err.code


@app.errorhandler(404)
def not_found_error(error):
    return "404, Nothing to see here!", 404
