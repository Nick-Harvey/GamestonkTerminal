from datetime import datetime, timedelta

from matplotlib import pyplot as plt

import bots.config_discordbot as cfg
import bots.helpers
from bots.config_discordbot import logger
from bots.helpers import image_border
from gamestonk_terminal.common.technical_analysis import volatility_model
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.helper_funcs import plot_autoscale


def donchian_command(
    ticker="", upper_length="25", lower_length="100", start="", end=""
):
    """Displays chart with donchian channel [Yahoo Finance]"""

    # Debug
    if cfg.DEBUG:
        logger.debug(
            "ta donchian %s %s %s %s %s",
            ticker,
            upper_length,
            lower_length,
            start,
            end,
        )

    # Check for argument
    if ticker == "":
        raise Exception("Stock ticker is required")

    if start == "":
        start = datetime.now() - timedelta(days=365)
    else:
        start = datetime.strptime(start, cfg.DATE_FORMAT)

    if end == "":
        end = datetime.now()
    else:
        end = datetime.strptime(end, cfg.DATE_FORMAT)

    if not upper_length.lstrip("-").isnumeric():
        raise Exception("Number has to be an integer")
    upper_length = float(upper_length)
    if not lower_length.lstrip("-").isnumeric():
        raise Exception("Number has to be an integer")
    lower_length = float(lower_length)

    ticker = ticker.upper()
    df_stock = bots.helpers.load(ticker, start)
    if df_stock.empty:
        raise Exception("Stock ticker is invalid")

    # Retrieve Data
    df_stock = df_stock.loc[(df_stock.index >= start) & (df_stock.index < end)]

    df_ta = volatility_model.donchian(
        df_stock["High"], df_stock["Low"], upper_length, lower_length
    )

    # Output Data
    fig, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    ax.plot(df_stock.index, df_stock["Adj Close"].values, color="k", lw=3)
    ax.plot(df_ta.index, df_ta.iloc[:, 0].values, "b", lw=1.5, label="upper")
    ax.plot(df_ta.index, df_ta.iloc[:, 1].values, "b", lw=1.5, ls="--")
    ax.plot(df_ta.index, df_ta.iloc[:, 2].values, "b", lw=1.5, label="lower")
    ax.set_title(f"{ticker} donchian")
    ax.set_xlim(df_stock.index[0], df_stock.index[-1])
    ax.set_xlabel("Time")
    ax.set_ylabel("Price ($)")

    ax.legend([ticker, df_ta.columns[0], df_ta.columns[1], df_ta.columns[2]])
    ax.fill_between(
        df_ta.index,
        df_ta.iloc[:, 0].values,
        df_ta.iloc[:, 2].values,
        alpha=0.1,
        color="b",
    )
    ax.grid(b=True, which="major", color="#666666", linestyle="-")

    plt.gcf().autofmt_xdate()
    fig.tight_layout(pad=1)

    plt.legend()
    imagefile = "ta_donchian.png"
    plt.savefig(imagefile)

    imagefile = image_border(imagefile)

    return {
        "title": f"Stocks: Donchian-Channels {ticker}",
        "imagefile": imagefile,
    }
