import logging
import os

from gamestonk_terminal.decorators import log_start_end
from gamestonk_terminal.decorators import check_api_key
from gamestonk_terminal.economy import finnhub_model
from gamestonk_terminal.helper_funcs import export_data, print_rich_table
from gamestonk_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
@check_api_key(["API_FINNHUB_KEY"])
def economy_calendar_events(country: str, num: int, impact: str, export: str):
    """Output economy calendar impact events. [Source: Finnhub]

    Parameters
    ----------
    country : str
        Country from where to get economy calendar impact events
    num : int
        Number economy calendar impact events to display
    impact : str
        Impact of the economy event
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    df_events = finnhub_model.get_economy_calendar_events()

    if df_events.empty:
        return

    df_econ_calendar = df_events[df_events["country"] == country].sort_values(
        "time", ascending=True
    )

    if df_econ_calendar.empty:
        console.print(
            "No latest economy calendar events found in the specified country\n"
        )
        return

    if impact != "all":
        df_econ_calendar = df_econ_calendar[df_econ_calendar["impact"] == impact]

        if df_econ_calendar.empty:
            console.print(
                "No latest economy calendar events found in the specified country with this impact\n"
            )
            return

    df_econ_calendar = df_econ_calendar.fillna("").head(n=num)

    d_econ_calendar_map = {
        "actual": "Actual release",
        "prev": "Previous release",
        "country": "Country",
        "unit": "Unit",
        "estimate": "Estimate",
        "event": "Event",
        "impact": "Impact Level",
        "time": "Release time",
    }

    df_econ_calendar = df_econ_calendar[
        ["time", "event", "impact", "prev", "estimate", "actual", "unit"]
    ].rename(columns=d_econ_calendar_map)

    df_econ_calendar.replace("", float("NaN"), inplace=True)
    df_econ_calendar.dropna(how="all", axis=1, inplace=True)

    print_rich_table(
        df_econ_calendar,
        headers=list(df_econ_calendar.columns),
        show_index=False,
        title="Economy Calendar",
    )
    console.print("")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "events",
        df_econ_calendar,
    )
