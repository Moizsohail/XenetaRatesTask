from typing import Any, List, Tuple
import application as app


def to_sql_array(
    arr: List[Any],
) -> Tuple[str]:
    return [f"'{x}'" for x in arr]


def debug_log(func):
    def inner(*arg, **kwargs):

        app.app_logger.debug(
            f"{func.__name__} :: {arg[:]}\n",
        )
        return func(*arg, **kwargs)

    return inner
