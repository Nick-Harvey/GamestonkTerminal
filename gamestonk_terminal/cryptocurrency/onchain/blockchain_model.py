"""Blockchain model"""
__docformat__ = "numpy"

import logging

import pandas as pd
import requests

from gamestonk_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def _make_request(endpoint: str) -> dict:
    """Helper method handles Blockchain API requests. [Source: https://api.blockchain.info/]

    Parameters
    ----------
    endpoint: str
        endpoint url
    Returns
    -------
    dict:
        dictionary with response data
    """

    url = f"https://api.blockchain.info/{endpoint}"
    response = requests.get(
        url, headers={"Accept": "application/json", "User-Agent": "GST"}
    )
    if not 200 <= response.status_code < 300:
        raise Exception(f"fcd terra api exception: {response.text}")
    try:
        return response.json()
    except Exception as e:
        logger.exception("Invalid Response: %s", str(e))
        raise ValueError(f"Invalid Response: {response.text}") from e


@log_start_end(log=logger)
def get_btc_circulating_supply() -> pd.DataFrame:
    """Returns BTC circulating supply [Source: https://api.blockchain.info/]

    Returns
    -------
    pd.DataFrame
        BTC circulating supply
    """

    data = _make_request(
        "charts/total-bitcoins?timespan=all&sampled=true&metadata=false&cors=true&format=json"
    )["values"]
    df = pd.DataFrame(data)
    df["x"] = df["x"] * 1_000_000_000
    df["x"] = pd.to_datetime(df["x"])
    return df


@log_start_end(log=logger)
def get_btc_confirmed_transactions() -> pd.DataFrame:
    """Returns BTC confirmed transactions [Source: https://api.blockchain.info/]

    Returns
    -------
    pd.DataFrame
        BTC confirmed transactions
    """

    data = _make_request(
        "charts/n-transactions?timespan=all&sampled=true&metadata=false&cors=true&format=json"
    )["values"]
    df = pd.DataFrame(data)
    df["x"] = df["x"] * 1_000_000_000
    df["x"] = pd.to_datetime(df["x"])
    return df
