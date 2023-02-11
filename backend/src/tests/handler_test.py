import json
import pytest
from flask.testing import FlaskClient


def test_get_rates_api__with_sql_injection(
    client: FlaskClient,
):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-20&origin=;DROP"
        " TABLE;&&destination=scandinavia"
    )
    assert response.status_code == 400
    data = json.loads(response.get_data())
    assert (
        data["message"]
        == "Invalid type: Origin should be string"
    )


def test_get_rates_api(client: FlaskClient):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-20&origin=CNCWN&destination=scandinavia"
    )
    assert response.status_code == 200
    data = json.loads(response.get_data())
    assert len(data) == 18


def test_get_rates_api__null_case(client: FlaskClient):
    # used the following query to find origin_codes and dest_codes
    # SELECT orig_code, dest_code, day
    # FROM prices
    # GROUP BY orig_code, dest_code, day
    # HAVING COUNT(*) < 3
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-20&origin=CNSGH&destination=LVRIX"
    )
    assert response.status_code == 200
    data = json.loads(response.get_data())
    assert len(data) == 18
    total_non_null_average_price = len(
        [
            row
            for row in data
            if row["average_price"] != None
        ]
    )

    assert total_non_null_average_price == 0


@pytest.mark.parametrize(
    "date_from, date_to, origin, destination,"
    " status_code, error_message",
    [
        (
            None,  # missing date_from case
            "2016-01-20",
            "CNCWN",
            "scandinavia",
            400,
            "Invalid Argument: date_from Not Found",
        ),
        (
            "2016-01-01",  # missing orig_code case
            "2016-01-20",
            None,
            "scandinavia",
            400,
            "Invalid Argument: origin Not Found",
        ),
        (
            "2016-01-01",  # invalid origin type case
            "2016-01-20",
            10,
            "scandinavia",
            400,
            "Invalid type: Origin should be string",
        ),
        (
            "2016-01-01",  # unkown origin_code case
            "2016-01-20",
            "doesnt_exist",
            "scandinavia",
            404,
            "doesnt_exist: Port/Region doesn't exist",
        ),
    ],
)
def test_get_rates_api__failure_states(
    client: FlaskClient,
    date_from,
    date_to,
    origin,
    destination,
    status_code,
    error_message,
):
    params = {}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    if origin:
        params["origin"] = origin
    if destination:
        params["destination"] = destination

    endpoint = "/rates?" + "&".join(
        [f"{k}={v}" for k, v in params.items()]
    )
    response = client.get(endpoint)
    assert response.status_code == status_code
    data = json.loads(response.get_data())
    assert data["message"] == error_message
