from datetime import date
from unittest.mock import MagicMock
from accessors import get_db
from accessors.accessors import (
    get_average_prices_by_day,
    get_port_codes_from_region_slug,
    verify_port_code,
)
from application import app
from shared.constants import MIN_PRICES_BEFORE_NULL
from shared.specs import (
    GetPricesByDayParams,
    GetPricesResponse,
    VerifyPortCodeParams,
)
import pytest


@pytest.mark.parametrize(
    "country, expected_codes",
    [
        (
            "america",  # should include north-america,texas,south-america
            [
                "AME",
                "NYC",
                "TEX",
                "LAX",
                "MIA",
                "SAO",
                "LIM",
            ],
        ),
        (
            "texas",  # should include texas
            [
                "TEX",
            ],
        ),
        (
            "north-america",  # should include north-america,texas
            ["NYC", "TEX", "LAX", "MIA"],
        ),
        (
            "south-america",  # should include south-america
            ["SAO", "LIM"],
        ),
    ],
)
def test_get_port_codes_from_region_slug__recursively_find_parents(
    country, expected_codes
):
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            regions = [
                ("america", "a", None),
                ("north-america", "a", "america"),
                ("texas", "a", "north-america"),
                ("south-america", "a", "america"),
            ]
            ports = [
                ("AME", "a", "america"),
                ("NYC", "a", "north-america"),
                ("TEX", "a", "texas"),
                ("LAX", "a", "north-america"),
                ("MIA", "a", "north-america"),
                ("SAO", "a", "south-america"),
                ("LIM", "a", "south-america"),
            ]

            cursor.executemany(
                "INSERT INTO regions (slug, name,"
                " parent_slug) VALUES (%s, %s, %s)",
                regions,
            )
            cursor.executemany(
                "INSERT INTO ports (code, name,"
                " parent_slug) VALUES (%s, %s, %s)",
                ports,
            )

            result = get_port_codes_from_region_slug(
                cursor, country
            )

            assert result == expected_codes

            # Please note that I have specifically not added
            # commit at this point as I wanted to remove
            # the freshly added regions and ports.
            cursor.execute("DELETE FROM prices")
            cursor.execute("DELETE FROM ports")
            cursor.execute("DELETE FROM regions")


def test_get_port_codes_from_region_slug__passing_in_port_code():

    slug = "CNYTN"
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            result = get_port_codes_from_region_slug(
                cursor, slug
            )

            assert len(result) == 0


def test_get_average_prices_by_day__results():
    params = GetPricesByDayParams(
        start_date="2016-01-10",
        end_date="2016-01-19",
        orig_codes=["CNYTN"],
        dest_codes=["ESBIO"],
    )
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            result = get_average_prices_by_day(
                cursor, params
            )

            assert len(result) == 10


def test_get_average_prices_by_day__no_results():
    params = GetPricesByDayParams(
        start_date="2016-01-10",
        end_date="2016-01-19",
        orig_codes=["unkown"],
        dest_codes=["ESBIO"],
    )
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            result = get_average_prices_by_day(
                cursor, params
            )

            assert len(result) == 0


def test_get_average_prices_by_day__multiple_codes():
    params = GetPricesByDayParams(
        start_date="2016-01-10",
        end_date="2016-01-19",
        orig_codes=["CNYTN", "CNXAM"],
        dest_codes=["ESBIO", "NOORK"],
    )
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            result = get_average_prices_by_day(
                cursor, params
            )

            assert len(result) == 10


def test_get_average_prices_by_day__null_average_case():
    params = GetPricesByDayParams(
        start_date="2021-01-01",
        end_date="2021-01-03",
        orig_codes=["NOR", "SWE"],
        dest_codes=["OSL", "STO"],
    )
    prices = [
        (date(2021, 1, 1), 50, 1),
        (date(2021, 1, 2), 100, 2),
        (date(2021, 1, 3), 200, MIN_PRICES_BEFORE_NULL),
    ]

    cursor = MagicMock()
    cursor.fetchall.return_value = prices
    result = get_average_prices_by_day(cursor, params)

    expected_result = [
        GetPricesResponse(
            day="2021-01-01", average_price=None
        ),
        GetPricesResponse(
            day="2021-01-02", average_price=None
        ),
        GetPricesResponse(
            day="2021-01-03", average_price=200
        ),
    ]

    assert result == expected_result


def test_verify_port_code__exists():
    params = VerifyPortCodeParams(
        orig="CNYTN", dest="NOORK"
    )
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            result = verify_port_code(cursor, params)

            assert result.orig_code_exists
            assert result.dest_code_exists


def test_verify_port_code__not_found():
    params = VerifyPortCodeParams(
        orig="not found", dest="not found"
    )
    with app.app_context():
        db = get_db()
        with db.cursor() as cursor:
            result = verify_port_code(cursor, params)

            assert not result.orig_code_exists
            assert not result.dest_code_exists
