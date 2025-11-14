# ercot_emil/api.py
from __future__ import annotations

from datetime import date
from typing import Optional
import pandas as pd

from .client import get_report_df


def get_np3_agg_as_offers_ecrsm(
    delivery_date_from: date,
    delivery_date_to: Optional[date] = None,
    ecrsm_offer_price_from: Optional[float] = None,
    ecrsm_offer_price_to: Optional[float] = None,
    hour_ending_from: Optional[int] = None,
    hour_ending_to: Optional[int] = None,
    mw_offered_from: Optional[float] = None,
    mw_offered_to: Optional[float] = None,
    page: Optional[int] = None,
    size: Optional[int] = 1000,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
) -> pd.DataFrame:
    """
    NP3-911-ER / 2d_agg_as_offers_ecrsm report.
    Docs params: ECRSMOfferPriceFrom/To, deliveryDateFrom/To, hourEndingFrom/To, MWOfferedFrom/To, page, size, sort, dir
    """

    if delivery_date_to is None:
        delivery_date_to = delivery_date_from

    params = {
        "deliveryDateFrom": delivery_date_from.strftime("%Y-%m-%d"),
        "deliveryDateTo": delivery_date_to.strftime("%Y-%m-%d"),
    }

    # Only add params the user passed in
    if ecrsm_offer_price_from is not None:
        params["ECRSMOfferPriceFrom"] = ecrsm_offer_price_from
    if ecrsm_offer_price_to is not None:
        params["ECRSMOfferPriceTo"] = ecrsm_offer_price_to
    if hour_ending_from is not None:
        params["hourEndingFrom"] = hour_ending_from
    if hour_ending_to is not None:
        params["hourEndingTo"] = hour_ending_to
    if mw_offered_from is not None:
        params["MWOfferedFrom"] = mw_offered_from
    if mw_offered_to is not None:
        params["MWOfferedTo"] = mw_offered_to
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    if direction is not None:
        params["dir"] = direction

    return get_report_df(
        "/public-reports/np3-911-er/2d_agg_as_offers_ecrsm",
        params=params,
    )
