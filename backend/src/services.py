from typing import List
from accessors import get_db
from accessors.accessors import (
    get_port_codes_from_region_slug,
    get_average_prices_by_day,
    verify_port_code,
    verify_region_slug,
)
from shared.specs import (
    GetApiRatesParams,
    GetPricesByDayParams,
    GetPricesResponse,
    VerifyPortCodeParams,
)
from validators import NotFoundException


def _convert_slugs_to_port_codes(
    cursor, orig: str, dest: str
):
    spec = VerifyPortCodeParams(orig=orig, dest=dest)
    port_code_verified = verify_port_code(cursor, spec)
    orig_codes = [orig]
    dest_codes = [dest]
    if not port_code_verified.orig_code_exists:
        if not verify_region_slug(cursor, orig):
            raise NotFoundException(
                f"{orig}: Port/Region doesn't exist"
            )

        orig_codes = get_port_codes_from_region_slug(
            cursor, orig
        )
    if not port_code_verified.dest_code_exists:
        if not verify_region_slug(cursor, dest):
            raise NotFoundException(
                f"{dest}: Port/Region doesn't exist"
            )
        dest_codes = get_port_codes_from_region_slug(
            cursor, dest
        )

    return orig_codes, dest_codes


def get_api_rates(
    params: GetApiRatesParams,
) -> List[GetPricesResponse]:
    db = get_db()
    prices = []
    with db.cursor() as cursor:
        [
            orig_codes,
            dest_codes,
        ] = _convert_slugs_to_port_codes(
            cursor, params.orig, params.dest
        )

        prices = get_average_prices_by_day(
            cursor,
            GetPricesByDayParams(
                start_date=params.date_from,
                end_date=params.date_to,
                orig_codes=orig_codes,
                dest_codes=dest_codes,
            ),
        )
    return prices
