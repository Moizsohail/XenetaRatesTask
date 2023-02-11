from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GetPricesByDayParams:
    start_date: str
    end_date: str
    orig_codes: List[str]
    dest_codes: List[str]


@dataclass
class GetPricesResponse:
    average_price: Optional[float]
    day: str


@dataclass
class GetApiRatesParams:
    date_from: str
    date_to: str
    orig: str
    dest: str


@dataclass
class VerifyPortCodeParams:
    orig: str
    dest: str


@dataclass
class VerifyPortCodeResponse:
    orig_code_exists: bool
    dest_code_exists: bool


@dataclass
class GetApiRatesQuery:
    date_from: str
    date_to: str
    origin: str
    destination: str
