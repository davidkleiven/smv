import pandas as pd
from smv.constants import DATE, AREA_NUM
from smv import raw_plot, parametric_plot


def example_data() -> pd.DataFrame:
    """
    Create an example dataset. Each entry has a timestamp a data field and
    an area number.
    """
    items = []

    for i in range(0, 10):
        items.append({
            DATE: f'2018-10-{10+i}',
            'price': i**2,
            'string_field': 'some_text',
            AREA_NUM: int(i/4),
            'type': 'market'
        })

    for i in range(0, 10):
        items.append({
            DATE: f'2018-10-{11+i}',
            'precipitation': i,
            AREA_NUM: int(i/4),
            'type': 'met'
        })
    return pd.DataFrame(items)


def test_raw_plot():
    df = example_data()

    # Case 1: Check valid query
    series = [
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 0'
        },
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 1'
        }
    ]

    fig = raw_plot(df, DATE, 'price', series)
    assert len(fig.data) == 2
    assert len(fig.data[0]['x']) == 8
    assert len(fig.data[0]['y']) == 8
    assert len(fig.data[1]['x']) == 8
    assert len(fig.data[1]['y']) == 8

    # Case 2: Check when asking for area number that does not exist
    series = [
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 0'
        },
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 9'
        }
    ]

    # Expect only one empty dataset
    fig = raw_plot(df, DATE, 'price', series)
    assert len(fig.data) == 2
    assert len(fig.data[0]['x']) == 8
    assert len(fig.data[0]['y']) == 8
    assert len(fig.data[1]['x']) == 0
    assert len(fig.data[1]['y']) == 0

    # Case 3: Check when field in query does not exist
    series = [
        {
            'name': 'A1',
            'query': 'does_not_exist == 0'
        },
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 1'
        }
    ]

    # Expect only one dataset
    fig = raw_plot(df, DATE, 'price', series)
    assert len(fig.data) == 1

    # Case 4: Test if user asks for plotting non-numerical type. The expected behavior
    # is no crash, if plotly non-numerical types we just let it do what it does. The main
    # point of this test is to confirm that it does not crash
    series = [
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 0'
        },
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 1'
        }
    ]

    fig = raw_plot(df, DATE, 'string_field', series)
    assert len(fig.data) == 2

    # Case 5: Check if x-field does not exist. Expect an empty figure
    fig = raw_plot(df, 'does_not_exist', 'price', series)
    assert len(fig.data) == 0

    # Case 6: Check invalid series
    series = [
        {
            'series_name': 'A1',  # Should be name, not series_name
            'query': f'{AREA_NUM} == 0'
        },
        {
            'name': 'A1',
            'query': f'{AREA_NUM} == 1'
        }
    ]
    fig = raw_plot(df, 'does_not_exist', 'price', series)
    assert len(fig.data) == 0


def test_parametric_plot():
    df = example_data()

    # Case 1: Test valid query
    fig = parametric_plot(df, {
        'field': 'price',
        'query': "type == 'market'"
    }, {
        'field': 'precipitation',
        'query': "type == 'met'"
    }
    )

    assert len(fig.data) == 1
    assert len(fig.data[0]['x']) == 10
    assert len(fig.data[0]['y']) == 10

    # Case 2: Test non-existing x-field
    fig = parametric_plot(df, {
        'field': 'does_not_exist',
        'query': "type == 'market'"
    }, {
        'field': 'precipitation',
        'query': "type == 'met'"
    }
    )
    assert len(fig.data) == 0

    # Case 3: Test non-existing y-field
    fig = parametric_plot(df, {
        'field': 'price',
        'query': "type == 'market'"
    }, {
        'field': 'does_not_exist',
        'query': "type == 'met'"
    }
    )
    assert len(fig.data) == 0

    # Case 4: Missing query
    fig = parametric_plot(df, {
        'field': 'price',
    }, {
        'field': 'does_not_exist',
        'query': "type == 'met'"
    }
    )
    assert len(fig.data) == 0

    # Case 5: String field requested (can't interpolate in this case, so we expect no data)
    fig = parametric_plot(df, {
        'field': 'string_field',
        'query': "type == 'market'"
    }, {
        'field': 'does_not_exist',
        'query': "type == 'met'"
    }
    )
    assert len(fig.data) == 0
