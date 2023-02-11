from typing import List
from shared.utils import debug_log
from shared.constants import (
    MIN_PRICES_BEFORE_NULL,
)
from shared.specs import (
    GetPricesByDayParams,
    GetPricesResponse,
    VerifyPortCodeParams,
    VerifyPortCodeResponse,
)


def _get_region_descendents(cursor, parent_slug):
    # recursively get all child_slugs
    # Resource used: https://learnsql.com/blog/sql-recursive-cte/

    # I have added a recursive logic because if a user is looking for a cost to/from
    # a country. It should be acceptable to include charges to/from a city within that country.
    cursor.execute(
        """
            with recursive slugs as (select slug from regions where parent_slug = %s
                union all 
                
                select regions.slug from regions, slugs
                where slugs.slug  = regions.parent_slug 
            )
            select slug from slugs;
        """,
        (parent_slug,),
    )
    data = cursor.fetchall()
    if len(data) == 0:
        return []
    slugs_with_parent_selected_slug = [
        row[0] for row in data
    ]
    return slugs_with_parent_selected_slug


@debug_log
def get_port_codes_from_region_slug(
    cursor, selected_slug
) -> List[str]:
    descendent_slug = _get_region_descendents(
        cursor, selected_slug
    ) + [selected_slug]

    if len(selected_slug) == 0:
        return []

    cursor.execute(
        f"""
        SELECT code FROM ports WHERE parent_slug = ANY(%s);
        """,
        (descendent_slug,),
    )
    port_codes = [str(row[0]) for row in cursor.fetchall()]
    return port_codes


@debug_log
def verify_port_code(
    cursor, params: VerifyPortCodeParams
) -> VerifyPortCodeResponse:
    sql: str = """
            SELECT code FROM ports WHERE code = %s or code = %s;
        """
    cursor.execute(sql, (params.orig, params.dest))
    codes = [code[0] for code in cursor.fetchall()]

    response = VerifyPortCodeResponse(
        orig_code_exists=params.orig in codes,
        dest_code_exists=params.dest in codes,
    )

    return response


@debug_log
def verify_region_slug(cursor, region_slug: str) -> bool:
    sql: str = """
            SELECT slug FROM regions WHERE slug = %s;
        """
    cursor.execute(sql, (region_slug,))
    return len([slug for slug in cursor.fetchall()]) == 1


@debug_log
def get_average_prices_by_day(
    cursor, params: GetPricesByDayParams
) -> List[GetPricesResponse]:
    # This task can be accomplished in a single SQL. But I have broken it
    # down to accomodate readability

    # recursively get all child_slugs
    # Resource used: https://learnsql.com/blog/sql-recursive-cte/
    sql: str = """
            SELECT day, AVG(price), COUNT(price)
            FROM prices
            WHERE day BETWEEN %s AND %s
            AND orig_code = ANY(%s)
            AND dest_code = ANY(%s)
            GROUP BY day
            ORDER BY day
        """

    cursor.execute(
        sql,
        (
            params.start_date,
            params.end_date,
            params.orig_codes,
            params.dest_codes,
        ),
    )

    data = cursor.fetchall()

    return list(
        [
            GetPricesResponse(
                day=row[0].strftime("%Y-%m-%d"),
                average_price=round(float(row[1]))
                if row[2] >= MIN_PRICES_BEFORE_NULL
                else None,
            )
            for row in data
        ]
    )
