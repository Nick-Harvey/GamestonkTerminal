"""Portfolio analysis context API."""
import os
from gamestonk_terminal.helper_classes import ModelsNamespace as _models

# flake8: noqa
# pylint: disable=unused-import

# Context menus
from gamestonk_terminal.portfolio.portfolio_analysis.portfolio_view import (
    display_group_holdings as group,
)


# Models
models = _models(os.path.abspath(os.path.dirname(__file__)))
