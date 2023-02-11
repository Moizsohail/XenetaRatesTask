from typing import Any, List, Tuple
import application as app


def to_sql_array(
    arr: List[Any],
) -> Tuple[str]:
    return [f"'{x}'" for x in arr]


# def optimize_array(arr: List[Any]) -> str:
#     if len(arr) == 1:
#         return f" = '{arr[0]}'"

#     sql_string = convert_array_to_sql_string(arr)
#     return f" IN ({sql_string})"


def debug_log(func):
    def inner(*arg, **kwargs):

        app.app_logger.debug(
            f"{func.__name__} :: {arg[:]}\n",
        )
        return func(*arg, **kwargs)

    return inner
