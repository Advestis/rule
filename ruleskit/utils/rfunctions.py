import numpy as np
from typing import Union


def conditional_mean(activation: Union[np.ndarray, None], y: np.ndarray) -> float:
    """Mean of all activated values

    If activation is None, we assume the given y have already been extracted from the activation vector,
    which saves time.
    """
    if activation is None:
        return float(np.nanmean(y))

    if isinstance(activation, np.ndarray):
        y_conditional = np.extract(activation, y)
    else:
        raise TypeError("'activation' in conditional_mean must be None or a np.ndarray")
    return float(np.nanmean(y_conditional))


def conditional_std(activation: Union[np.ndarray, None], y: np.ndarray) -> float:
    """Standard deviation of all activated values

    If activation is None, we assume the given y have already been extracted from the activation vector,
    which saves time.
    """
    if activation is None:
        return float(np.nanstd(y))

    if isinstance(activation, np.ndarray):
        y_conditional = np.extract(activation, y)
    else:
        raise TypeError("'activationt' in conditional_std must be None or a np.ndarray")
    return float(np.nanstd(y_conditional))


def mse_function(prediction_vector: np.ndarray, y: np.ndarray) -> float:
    """
    Compute the mean squared error
    "$ \\dfrac{1}{n} \\Sigma_{i=1}^{n} (\\hat{y}_i - y_i)^2 $"

    Parameters
    ----------
    prediction_vector : np.ndarray
        A predictor vector. It means a sparse array with two
        different values ymean, if the rule is not active
        and the prediction is the rule is active.

    y : np.ndarray
        The real target values (real numbers)

    Return
    ------
    criterion : float
        the mean squared error
    """
    if len(prediction_vector) != len(y):
        raise ValueError("The two array must have the same length")
    error_vector = prediction_vector - y
    criterion = np.nanmean(error_vector ** 2)
    # noinspection PyTypeChecker
    return criterion


def mae_function(prediction_vector: np.ndarray, y: np.ndarray) -> float:
    """
    Compute the mean absolute error
    "$ \\dfrac{1}{n} \\Sigma_{i=1}^{n} |\\hat{y}_i - y_i| $"

    Parameters
    ----------
    prediction_vector : np.ndarray
        A predictor vector. It means a sparse array with two
        different values ymean, if the rule is not active
        and the prediction is the rule is active.

    y : np.ndarray
        The real target values (real numbers)

    Return
    ------
    criterion : float
        the mean absolute error
    """
    if len(prediction_vector) != len(y):
        raise ValueError("The two array must have the same length")
    error_vect = np.abs(prediction_vector - y)
    criterion = np.nanmean(error_vect)
    # noinspection PyTypeChecker
    return criterion


def aae_function(prediction_vector: np.ndarray, y: np.ndarray) -> float:
    """
    Compute the mean squared error
    "$ \\dfrac{1}{n} \\Sigma_{i=1}^{n} (\\hat{y}_i - y_i)$"

    Parameters
    ----------
    prediction_vector : np.ndarray
        A predictor vector. It means a sparse array with two
        different values ymean, if the rule is not active
        and the prediction is the rule is active.

    y : np.ndarray
        The real target values (real numbers)

    Return
    ------
    criterion : float
        the mean squared error
    """
    if len(prediction_vector) != len(y):
        raise ValueError("The two array must have the same length")
    error_vector = np.mean(np.abs(prediction_vector - y))
    median_error = np.mean(np.abs(y - np.median(y)))
    return error_vector / median_error


def calc_criterion(prediction_vector: np.ndarray, y: np.ndarray, method: str, cond: bool = True) -> float:
    """
    Compute the criteria

    Parameters
    ----------
    prediction_vector : np.ndarray
        The prediction vector

    y : np.ndarray
        The real target values (real numbers)

    method : str
        The method mse_function or mse_function criterion

    cond : bool
        To evaluate the criterion only if the rule is activated

    Return
    ------
    criterion : float
        Criteria value
    """
    if cond:
        sub_y = np.extract(prediction_vector != 0, y)
        sub_pred = np.extract(prediction_vector != 0, prediction_vector)
    else:
        sub_y = y
        sub_pred = prediction_vector

    if method.lower() == "mse":
        criterion = mse_function(sub_pred, sub_y)

    elif method.lower() == "mae":
        criterion = mae_function(sub_pred, sub_y)

    elif method.lower() == "aae":
        criterion = aae_function(sub_pred, sub_y)

    else:
        raise ValueError(f"Unknown criterion: {method}. Please choose among mse, mae and aae")

    return criterion
