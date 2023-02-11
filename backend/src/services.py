from typing import List
from accessors import get_db
from accessors.accessors import (
    get_port_codes_from_region_slug,
    get_average_prices_service,
    verify_port_code,
)
from shared.specs import (
    GetApiRatesParams,
    GetPricesParams,
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
        orig_codes = get_port_codes_from_region_slug(
            cursor, orig
        )
    if not port_code_verified.dest_code_exists:
        dest_codes = get_port_codes_from_region_slug(
            cursor, dest
        )

    if len(orig_codes) == 0:
        raise NotFoundException(
            f"{orig}: Is neither a region or a port code"
        )

    if len(dest_codes) == 0:
        raise NotFoundException(
            f"{dest}: Is neither a region or a port code"
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

        prices = get_average_prices_service(
            cursor,
            GetPricesParams(
                start_date=params.date_from,
                end_date=params.date_to,
                orig_codes=orig_codes,
                dest_codes=dest_codes,
            ),
        )
    return prices
