from datetime import datetime
import re
from flask import request
from shared.specs import GetApiRatesQuery


class APIException(Exception):
    code = 400
    description = "Error"


class APIValidationError(APIException):
    code = 400
    description = "Validation Error"


class NotFoundException(APIException):
    code = 404
    description = "Not Found"


def validate_date(date_text: str, field_name: str):
    try:
        return datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise APIValidationError(
            f"Incorrect date format for {field_name},"
            " should be YYYY-MM-DD"
        )


def validate_date_range(
    date_from: datetime, date_to: datetime
):

    if date_from > date_to:
        raise APIValidationError(
            "Date From can't be greater than Date To"
        )


def validate_strings(string_text, field_name):
    if not isinstance(string_text, str) or not re.match(
        "^[A-Za-z_]*$", string_text
    ):
        raise APIValidationError(
            f"Invalid type: {field_name} should be string"
        )


def get_api_rates_query_validator(func):
    def validated():
        try:
            date_from = request.args["date_from"]
            date_to = request.args["date_to"]
            origin = request.args["origin"]
            destination = request.args["destination"]

            validate_date_range(
                validate_date(date_from, "date_from"),
                validate_date(date_to, "date_to"),
            )
            validate_strings(origin, "Origin")
            validate_strings(destination, "Destination")

            spec = GetApiRatesQuery(
                date_from=date_from,
                date_to=date_to,
                origin=origin,
                destination=destination,
            )
            return func(spec)

        except KeyError as e:
            key = e.args[0]
            raise APIValidationError(
                f"Invalid Argument: {key} Not Found"
            )

    return validated
