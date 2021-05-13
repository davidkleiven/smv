from smv.util import deseasonalize, add_deseasonalized_value
import numpy as np
import pandas as pd


def periodic_signal(period: float):
    num_points = 40
    t = [f'0:0:{i}' for i in range(num_points)]
    y = [np.cos(2.0*np.pi*x/period) for x in range(num_points)]
    return t, y


def test_deseasonalize():
    period = 5
    t, y = periodic_signal(period)

    res = deseasonalize(t, y, "%H:%M:%S", period)
    nans = res[:period]
    non_nans = res[period:]
    assert all(np.isnan(x) for x in nans)
    assert np.allclose(non_nans, 0.0)


def test_update_by_index():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [2, 3, 4]})
    subset = df.query("A == 2")
    subset["B"] = [10]

    df.update(subset)
    expect = pd.DataFrame({"A": [1, 2, 3], "B": [2, 10, 4]})
    assert np.allclose(df["A"], expect["A"])
    assert np.allclose(df["B"], expect["B"])


def test_add_deseasonalized():
    period = 5
    t, y = periodic_signal(period)

    df = pd.DataFrame({
        'timestamp': t,
        'periodic_signal': y
    })

    df = add_deseasonalized_value(df, 'timestamp', 'periodic_signal', '%H:%M:%S', period)

    assert len(df.columns) == 3
    expect_cols = ['timestamp', 'periodic_signal', 'periodic_signal_deseasonalized']
    assert all(x == y for x, y in zip(df.columns, expect_cols))

    nans = df['periodic_signal_deseasonalized'][:period]
    non_nans = df['periodic_signal_deseasonalized'][period:]
    assert len(nans) == period
    assert len(non_nans) == len(y) - period
    assert all(np.isnan(x) for x in nans)
    assert np.allclose(non_nans, 0.0)
