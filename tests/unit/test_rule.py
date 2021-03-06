from ruleskit import HyperrectangleCondition
from ruleskit import Rule
import numpy as np
import pytest


@pytest.mark.parametrize(
    "x, y, condition, activation, compressed_activation, cov, pred",
    [
        (
            np.array([[1, 3], [3, 4], [2, np.nan]]),
            np.array([1, 3, 2]),
            HyperrectangleCondition([0], bmins=[1], bmaxs=[2]),
            np.array([1, 0, 1]),
            5,
            2/3,
            1.5,
        ),
        (
            np.array([[1, 3], [3, 4], [2, np.nan]]),
            np.array([1, 3, 2]),
            HyperrectangleCondition([1], bmins=[3], bmaxs=[5]),
            np.array([1, 1, 0]),
            6,
            2/3,
            2
        ),
        (
            np.array([[1, 3], [3, 4], [2, np.nan]]),
            np.array([1, 3, 2]),
            HyperrectangleCondition([0, 1], bmins=[1, 3], bmaxs=[2, 5]),
            np.array([1, 0, 0]),
            4,
            1/3,
            1
        ),
    ],
)
def test_activation(x, y, condition, activation, compressed_activation, cov, pred):
    rule = Rule(condition=condition)
    rule.fit(xs=x, y=y)
    np.testing.assert_equal(rule.activation, activation)
    np.testing.assert_equal(rule._activation.as_int, compressed_activation)
    np.testing.assert_equal(rule.coverage, cov)
    np.testing.assert_equal(rule.prediction, pred)


@pytest.mark.parametrize(
    "x, y, condition1, condition2, activation1, activation2, activation_test",
    [
        (
            np.array([[1, 3], [3, 4], [2, np.nan]]),
            np.array([1, 3, 2]),
            HyperrectangleCondition([0], bmins=[1], bmaxs=[2]),
            HyperrectangleCondition([1], bmins=[3], bmaxs=[5]),
            np.array([1, 0, 1]),
            np.array([1, 1, 0]),
            np.array([1, 0, 0]),
        ),
    ],
)
def test_add(x, y, condition1, condition2, activation1, activation2, activation_test):
    rule1 = Rule(condition=condition1)
    rule1.fit(xs=x, y=y)
    rule2 = Rule(condition=condition2)
    rule2.fit(xs=x, y=y)

    new_rule = rule1 + rule2
    np.testing.assert_equal(new_rule.activation, activation_test)
    new_rule.fit(xs=x, y=y)
    np.testing.assert_equal(new_rule.activation, activation_test)
