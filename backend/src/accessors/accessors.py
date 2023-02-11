from typing import List
from shared.utils import debug_log, to_sql_array
from shared.constants import (
    MIN_PRICES_BEFORE_NULL,
)
from shared.specs import (
    GetPricesParams,
    GetPricesResponse,
    VerifyPortCodeParams,
    VerifyPortCodeResponse,
)


import application as app


@debug_log
def get_port_codes_from_region_slug(
    cursor, selected_slug
) -> List[str]:
    # This task can be accomplished in a single SQL. But I have broken it
    # down to accomodate readability

    # recursively get all child_slugs
    # Resource used: https://learnsql.com/blog/sql-recursive-cte/

    cursor.execute(
        """
            with recursive slugs as (select slug from regions where parent_slug = %s
                union all 
                
                select regions.slug from regions, slugs
                where slugs.slug  = regions.parent_slug 
            )
            select slug from slugs;
        """,
        (selected_slug,),
    )
    data = cursor.fetchall()

    if len(data) == 0:
        return []

    slugs_with_parent_selected_slug = [
        row[0] for row in data
    ]

    cursor.execute(
        f"""
        SELECT code FROM ports WHERE parent_slug = ANY(%s);
        """,
        (to_sql_array(slugs_with_parent_selected_slug),),
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
def get_average_prices_service(
    cursor, params: GetPricesParams
):
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
            to_sql_array(params.orig_codes),
            to_sql_array(params.dest_codes),
        ),
    )

    data = cursor.fetchall()
    return list(
        [
            GetPricesResponse(
                day=row[0].strftime("%Y-%m-%d"),
                average_price=float(row[1])
                if row[2] > MIN_PRICES_BEFORE_NULL
                else None,
            )
            for row in data
        ]
    )
