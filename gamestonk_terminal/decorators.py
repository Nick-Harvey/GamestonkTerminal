"""Decorators"""
__docformat__ = "numpy"
import functools
import logging
import os
import pandas as pd

from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.rich_config import console

logger = logging.getLogger(__name__)


def log_start_end(func=None, log=None):
    """Wrap function to add a log entry at execution start and end.

    Parameters
    ----------
    func : optional
        Function, by default None
    log : optional
        Logger, by default None

    Returns
    -------
        Wrapped function
    """
    assert callable(func) or func is None  # nosec

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logging_name = ""

            args_passed_in_function = [
                repr(a) for a in args if isinstance(a, (pd.DataFrame, pd.Series)) or a
            ]

            if len(args) == 2 and (
                "__main__.TerminalController" in args_passed_in_function[0]
                or (
                    "gamestonk_terminal." in args_passed_in_function[0]
                    and "_controller" in args_passed_in_function[0]
                )
            ):
                logging_name = args_passed_in_function[0].split()[0][1:]
                args_passed_in_function = args_passed_in_function[1:]

            logger_used = logging.getLogger(logging_name) if logging_name else log

            logger_used.info(
                "START",
                extra={"func_name_override": func.__name__},
            )

            if os.environ.get("DEBUG_MODE") == "true":
                value = func(*args, **kwargs)
                log.info("END", extra={"func_name_override": func.__name__})
                return value
            try:
                value = func(*args, **kwargs)
                logger_used.info("END", extra={"func_name_override": func.__name__})
                return value
            except Exception as e:
                console.print(f"[red]Error: {e}\n[/red]")
                logger_used.exception(
                    "Exception: %s",
                    str(e),
                    extra={"func_name_override": func.__name__},
                )
                return []

        return wrapper

    return decorator(func) if callable(func) else decorator


# pylint: disable=import-outside-toplevel
def check_api_key(api_keys):
    """
    Wrapper around the view or controller function and
    print message statement to the console if API keys are not yet defined.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            if gtff.ENABLE_CHECK_API:
                import gamestonk_terminal.config_terminal as cfg

                undefined_apis = []
                for key in api_keys:
                    # Get value of the API Keys
                    if getattr(cfg, key) == "REPLACE_ME":
                        undefined_apis.append(key)

                if undefined_apis:
                    undefined_apis_name = ", ".join(undefined_apis)
                    console.print(
                        f"[red]{undefined_apis_name} not defined. "
                        "Set API Keys in config_terminal.py or under keys menu.[/red]\n"
                    )  # pragma: allowlist secret
                else:
                    func(*args, **kwargs)
            else:
                func(*args, **kwargs)

        return wrapper_decorator

    return decorator


def disable_check_api():
    gtff.ENABLE_CHECK_API = False
