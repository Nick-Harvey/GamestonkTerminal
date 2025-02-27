import datetime as dt
import json
import logging

import pandas as pd
import requests

from gamestonk_terminal import config_terminal as cfg
from gamestonk_terminal.decorators import log_start_end
from gamestonk_terminal.rich_config import console

logger = logging.getLogger(__name__)

api_url = "https://open-api.coinglass.com/api/pro/v1/"

INTERVALS = [0, 1, 2, 4]


@log_start_end(log=logger)
def get_open_interest_per_exchange(symbol: str, interval: int) -> pd.DataFrame:
    """Returns open interest by exchange for a certain symbol
    [Source: https://coinglass.github.io/API-Reference/]

    Parameters
    ----------
    symbol : str
        Crypto Symbol to search open interest futures (e.g., BTC)
    interval : int
        Interval frequency (e.g., 0)

    Returns
    -------
    pd.DataFrame
        open interest by exchange and price
    """

    url = (
        api_url
        + f"futures/openInterest/chart?&symbol={symbol.upper()}&interval={interval}"
    )

    headers = {"coinglassSecret": cfg.API_COINGLASS_KEY}

    response = requests.request("GET", url, headers=headers)
    df = pd.DataFrame()

    if response.status_code == 200:
        res_json = json.loads(response.text)

        if res_json["success"]:
            if "data" in res_json:
                data = res_json["data"]
                time = data["dateList"]
                time_new = []
                for elem in time:
                    time_actual = dt.datetime.utcfromtimestamp(elem / 1000)
                    time_new.append(time_actual)

                df = pd.DataFrame(
                    data={
                        "date": time_new,
                        "price": data["priceList"],
                        **data["dataMap"],
                    }
                )
                df = df.set_index("date")
            else:
                console.print(f"No data found for {symbol}.\n")
        else:
            if "secret invalid" in res_json["msg"]:
                console.print("[red]Invalid API Key[/red]\n")
            else:
                console.print(res_json["msg"])

    elif response.status_code == 429:
        console.print("[red]Exceeded number of calls per minute[/red]\n")
    elif response.status_code == 429:
        console.print(
            "[red]IP address autobanned for exceeding calls limit multiple times.[/red]\n"
        )

    return df
