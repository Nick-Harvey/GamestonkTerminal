# IMPORTATION STANDARD

# IMPORTATION THIRDPARTY

# IMPORTATION INTERNAL
from gamestonk_terminal.helper_classes import ModelsNamespace as _models
from gamestonk_terminal.stocks.fundamental_analysis.financial_modeling_prep import (
    fmp_api,
)


def test_models():
    assert isinstance(fmp_api.models, _models)
