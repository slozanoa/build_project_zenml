import logging
from zenml import step
import pandas as pd
from sklearn.base import RegressorMixin
from src.evaluation import RMSE, R2, MSE
from typing import Tuple
from typing_extensions import Annotated

@step
def evaluate_model(
    model: RegressorMixin, 
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Tuple[
    Annotated[float, "r2_score"],
    Annotated[float, "rmse"]
]:
    """
    Evaluates the model on the ingested data
    Args:
        df: the ingested data
    """

    prediction = model.predict(X_test)
    mse_class = MSE()
    mse = mse_class.calculate_scores(y_test, prediction)

    r2_class = R2()
    r2_score = r2_class.calculate_scores(y_test, prediction)

    rmse_class = RMSE()
    rmse = rmse_class.calculate_scores(y_test, prediction)

    return r2_score, rmse
